"""Utilities for generating embeddings with the BGE-M3 model.

This module provides a small wrapper around :class:`sentence_transformers.SentenceTransformer`
for easy use of the BAAI/bge-m3 model. Embeddings are cached at the module
level to avoid repeatedly loading the model in a multi-request environment.
"""
from __future__ import annotations

from typing import Iterable, List, Sequence
import threading

from sentence_transformers import SentenceTransformer

# Default HuggingFace model name
DEFAULT_MODEL_NAME = "BAAI/bge-m3"

# Cache for loaded models to avoid re-loading in repeated calls
_models: dict[str, SentenceTransformer] = {}
_models_lock = threading.Lock()

def _get_model(name: str = DEFAULT_MODEL_NAME) -> SentenceTransformer:
    """Load and cache the SentenceTransformer model."""
    if name not in _models:
        with _models_lock:
            if name not in _models:
                _models[name] = SentenceTransformer(name)
    return _models[name]


class BgeM3Embedder:
    """Encode text using the BGE-M3 model."""

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self.model = _get_model(model_name)

    @property
    def dimension(self) -> int:
        """Return embedding dimensionality."""
        return self.model.get_sentence_embedding_dimension()

    def embed(
        self,
        texts: Sequence[str] | str,
        batch_size: int = 32,
        normalize: bool = True,
    ) -> List[List[float]]:
        """Return embeddings for given text(s)."""
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(
            list(texts),
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
        )


def embed(
    texts: Sequence[str] | str,
    batch_size: int = 32,
    normalize: bool = True,
    model_name: str = DEFAULT_MODEL_NAME,
):
    """Convenience function for embedding without creating an instance."""
    return BgeM3Embedder(model_name).embed(texts, batch_size=batch_size, normalize=normalize)


if __name__ == "__main__":
    import sys
    data = sys.argv[1:] or ["Hello, world!"]
    vectors = embed(data)
    print(vectors.shape)
