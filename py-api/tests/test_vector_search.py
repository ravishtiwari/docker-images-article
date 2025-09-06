import pytest
from unittest.mock import Mock, patch
from app.services.vector_service import vector_service


def test_generate_embedding():
    """Test generating embeddings for text"""
    text = "The Matrix is a science fiction movie"
    embedding = vector_service.generate_embedding(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384  # Default dimension
    assert all(isinstance(x, float) for x in embedding)


def test_generate_embedding_empty_text():
    """Test generating embedding for empty text"""
    embedding = vector_service.generate_embedding("")

    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert all(x == 0.0 for x in embedding)


def test_generate_embeddings_batch():
    """Test generating embeddings for multiple texts"""
    texts = ["The Matrix", "Inception", "The Dark Knight"]

    embeddings = vector_service.generate_embeddings_batch(texts)

    assert len(embeddings) == 3
    assert all(len(emb) == 384 for emb in embeddings)
    assert all(isinstance(emb, list) for emb in embeddings)


def test_calculate_similarity():
    """Test calculating similarity between vectors"""
    # Create two similar vectors
    vector1 = [1.0, 0.0, 0.0]
    vector2 = [0.9, 0.1, 0.0]

    similarity = vector_service.calculate_similarity(vector1, vector2)

    assert isinstance(similarity, float)
    assert 0.0 <= similarity <= 1.0
    assert similarity > 0.8  # Should be high similarity


def test_calculate_similarity_identical_vectors():
    """Test similarity of identical vectors"""
    vector = [1.0, 2.0, 3.0]
    similarity = vector_service.calculate_similarity(vector, vector)

    assert abs(similarity - 1.0) < 1e-6  # Should be very close to 1.0


def test_calculate_similarity_zero_vectors():
    """Test similarity with zero vectors"""
    zero_vector = [0.0, 0.0, 0.0]
    other_vector = [1.0, 2.0, 3.0]

    similarity = vector_service.calculate_similarity(zero_vector, other_vector)
    assert similarity == 0.0


@patch("app.services.vector_service.SentenceTransformer")
def test_vector_service_initialization_failure(mock_transformer):
    """Test vector service initialization with model loading failure"""
    mock_transformer.side_effect = Exception("Model loading failed")

    from app.services.vector_service import VectorService

    service = VectorService()

    assert service.model is None

    # Should return zero vector when model is not available
    embedding = service.generate_embedding("test text")
    assert embedding == [0.0] * 384
