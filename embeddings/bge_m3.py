import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY


def embed_text(text: str):
    """Return embedding vector for given text."""
    resp = openai.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return resp.data[0].embedding
