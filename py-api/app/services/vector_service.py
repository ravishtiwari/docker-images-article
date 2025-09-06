from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class VectorService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize with a sentence transformer model"""
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Vector service initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Error initializing vector service: {e}")
            self.model = None

    def generate_embedding(self, text: str) -> List[float]:
        """Generate vector embedding for text"""
        if not self.model:
            logger.warning("Vector model not available, returning zero vector")
            return [0.0] * 384  # Default dimension

        try:
            # Clean and prepare text
            text = text.strip()
            if not text:
                return [0.0] * 384

            # Generate embedding
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return [0.0] * 384

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if not self.model:
            logger.warning("Vector model not available, returning zero vectors")
            return [[0.0] * 384 for _ in texts]

        try:
            embeddings = self.model.encode(texts)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return [[0.0] * 384 for _ in texts]

    def calculate_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            v1 = np.array(vector1)
            v2 = np.array(vector2)

            # Calculate cosine similarity
            dot_product = np.dot(v1, v2)
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)

            if norm_v1 == 0 or norm_v2 == 0:
                return 0.0

            similarity = dot_product / (norm_v1 * norm_v2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0


vector_service = VectorService()
