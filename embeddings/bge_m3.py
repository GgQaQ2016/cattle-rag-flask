import numpy as np


def embed_text(text: str):
    # Placeholder embedding using character ord values
    vec = np.frombuffer(text.encode('utf-8'), dtype=np.uint8).astype(float)
    if vec.size == 0:
        return np.zeros(1)
    return vec / np.linalg.norm(vec)
