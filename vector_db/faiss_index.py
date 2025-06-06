"""Minimal FAISS index placeholder."""

class SimpleIndex:
    def __init__(self):
        self._items = []

    def add(self, embedding, metadata):
        self._items.append((embedding, metadata))

    def search(self, embedding, top_k=5):
        # very naive search by length difference
        scored = [ (abs(e[0][0] - embedding[0]), meta) for e, meta in self._items ]
        scored.sort(key=lambda x: x[0])
        return [meta for _, meta in scored[:top_k]]
