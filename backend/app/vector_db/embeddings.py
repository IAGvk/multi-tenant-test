from sentence_transformers import SentenceTransformer, models
from transformers import AutoTokenizer, AutoModel
import torch

from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
import numpy as np

from app.core.logger import get_logger
logger = get_logger(__name__)  # Use the centralized logger





class VectorDBService:
    def __init__(self):
        # self.device = "cpu"
        # self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        # self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2").to(self.device)

        model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.model = model
        self.client = QdrantClient(host="qdrant", port=6333)
        self.collection_name = "architecture_reviews"

    def create_collection(self):
        """Create collection if it doesn't exist"""
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=qdrant_models.VectorParams(
                size=768, #bert # 384 for all-MiniLM-L6-v2 embedding size
                distance=qdrant_models.Distance.COSINE
            )
        )

    def get_embeddings(self, text: str) -> np.ndarray:
        """Generate embeddings for text"""
        # inputs = self.tokenizer([text], max_length=384, truncation=True, return_tensors='pt').to(self.device)
        # with torch.no_grad():
        #     embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        # return embeddings.cpu().numpy()[0]
        return self.model.encode(text)

    def search_similar(self, query_vector: np.ndarray, top_k: int = 3):
        """Search for similar vectors"""
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )