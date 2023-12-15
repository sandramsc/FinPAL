from qdrant_client import QdrantClient
import os

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_API_KEY:
    raise Exception("QDRANT_API_KEY is not set")
if not QDRANT_URL:
    raise Exception("QDRANT_URL is not set")

client = QdrantClient("localhost", port=6333)

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)
