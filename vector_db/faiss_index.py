import numpy as np
from typing import List

# Simple in-memory "vector DB" for demo
_vectors = []
_docs = []


def add_vector(vector: np.ndarray, doc: str):
    _vectors.append(vector)
    _docs.append(doc)


def search_vectors(vector: np.ndarray, topk: int = 3) -> List[str]:
    if not _vectors:
        return []
    sims = [float(np.dot(v, vector) / (np.linalg.norm(v) * np.linalg.norm(vector))) for v in _vectors]
    idxs = np.argsort(sims)[-topk:][::-1]
    return [_docs[i] for i in idxs]
