"""Utilities for managing FAISS vector indexes.

This module provides a small wrapper around `faiss` so the rest of the
application does not need to deal with the specifics of saving and
loading indexes.  It supports creating an index, adding vectors with
optional metadata and performing similarity search.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Tuple

import faiss
import numpy as np


class FaissIndex:
    """Simple persistent FAISS index wrapper."""

    def __init__(self, dim: int, index_path: str, metadata_path: str | None = None) -> None:
        self.dim = dim
        self.index_path = index_path
        self.metadata_path = metadata_path or f"{index_path}.meta.json"

        self.index: faiss.Index = faiss.IndexIDMap(faiss.IndexFlatL2(dim))
        self.id_to_meta: Dict[int, Any] = {}
        self.next_id = 0

        self._load()

    def _load(self) -> None:
        """Load index and metadata from disk if they exist."""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            if not isinstance(self.index, faiss.IndexIDMap):
                # ensure we can remove by id and keep track of ids
                self.index = faiss.IndexIDMap(self.index)
            self.next_id = int(self.index.ntotal)
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.id_to_meta = {int(k): v for k, v in data.items()}
            if self.id_to_meta:
                self.next_id = max(self.id_to_meta.keys()) + 1

    def save(self) -> None:
        """Persist index and metadata to disk."""
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.id_to_meta, f)

    # ------------------------------------------------------------------
    # Modification helpers
    # ------------------------------------------------------------------
    def add_vectors(self, vectors: Iterable[Iterable[float]], metas: Iterable[Any] | None = None) -> List[int]:
        """Add a batch of vectors with optional metadata.

        Args:
            vectors: Iterable of vectors with length `dim`.
            metas: Optional iterable with metadata items corresponding to the
                vectors.  The objects will be stored as JSON serialisable
                values.

        Returns:
            The integer ids assigned to the inserted vectors.
        """
        arr = np.asarray(list(vectors), dtype="float32")
        if arr.ndim != 2 or arr.shape[1] != self.dim:
            raise ValueError(f"expected vectors of shape (n, {self.dim})")

        count = arr.shape[0]
        ids = np.arange(self.next_id, self.next_id + count, dtype="int64")

        if metas is None:
            metas = [{} for _ in range(count)]
        for idx, meta in zip(ids, metas):
            self.id_to_meta[int(idx)] = meta

        self.index.add_with_ids(arr, ids)
        self.next_id += count
        self.save()
        return ids.tolist()

    def remove_vectors(self, ids: Iterable[int]) -> None:
        """Remove vectors by id."""
        id_array = np.fromiter(ids, dtype="int64")
        if len(id_array) == 0:
            return
        self.index.remove_ids(id_array)
        for _id in id_array:
            self.id_to_meta.pop(int(_id), None)
        self.save()

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------
    def search(self, vectors: Iterable[Iterable[float]], top_k: int = 5) -> List[List[Tuple[int, float, Any]]]:
        """Search for nearest neighbours of `vectors`.

        Args:
            vectors: Iterable of query vectors.
            top_k: Number of results to return per query.

        Returns:
            For each query vector a list of tuples ``(id, distance, metadata)``
            sorted by ascending distance.
        """
        arr = np.asarray(list(vectors), dtype="float32")
        if arr.ndim != 2 or arr.shape[1] != self.dim:
            raise ValueError(f"expected vectors of shape (n, {self.dim})")

        distances, idxs = self.index.search(arr, top_k)
        results: List[List[Tuple[int, float, Any]]] = []
        for ids_row, dist_row in zip(idxs, distances):
            row = []
            for _id, dist in zip(ids_row, dist_row):
                if _id == -1:
                    continue
                meta = self.id_to_meta.get(int(_id))
                row.append((int(_id), float(dist), meta))
            results.append(row)
        return results

    def __len__(self) -> int:  # pragma: no cover - simple helper
        return int(self.index.ntotal)
