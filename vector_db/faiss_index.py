import os
import pickle
from typing import List

import faiss
import numpy as np


class FaissIndex:
    def __init__(self, dim: int, index_file: str = "data/faiss_index.bin"):
        self.dim = dim
        self.index_file = index_file
        self.text_file = index_file + ".pkl"
        self.texts: List[str] = []
        if os.path.exists(index_file):
            self.load()
        else:
            self.index = faiss.IndexFlatL2(dim)

    def add(self, embeddings: List[List[float]], texts: List[str]):
        arr = np.array(embeddings).astype("float32")
        self.index.add(arr)
        self.texts.extend(texts)
        self.save()

    def search(self, embedding: List[float], k: int = 5) -> List[str]:
        if self.index.ntotal == 0:
            return []
        D, I = self.index.search(np.array([embedding]).astype("float32"), k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]

    def save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.text_file, "wb") as f:
            pickle.dump(self.texts, f)

    def load(self):
        self.index = faiss.read_index(self.index_file)
        if os.path.exists(self.text_file):
            with open(self.text_file, "rb") as f:
                self.texts = pickle.load(f)
        else:
            self.texts = []
