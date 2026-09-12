import numpy as np

from app.embedding_matcher import (
    generate_embedding,
    calculate_embedding_similarity
)


def test_generate_embedding():
    model = MockModel()

    embedding = generate_embedding(
        "Python developer",
        model
    )

    assert embedding is not None
    assert embedding.shape == (3,)


def test_generate_embedding_empty_text():
    model = MockModel()

    result = generate_embedding(
        "",
        model
    )

    assert result is None


def test_embedding_similarity_identical_vectors():
    embedding = np.array(
        [1.0, 0.0, 0.0]
    )

    result = calculate_embedding_similarity(
        embedding,
        embedding
    )

    assert result == 100.0


def test_embedding_similarity_empty_embeddings():
    result = calculate_embedding_similarity(
        None,
        np.array([1.0, 0.0, 0.0])
    )

    assert result == 0.0


class MockModel:

    def encode(
        self,
        text,
        convert_to_numpy=True
    ):
        return np.array(
            [1.0, 2.0, 3.0]
        )


def test_embedding_similarity_negative_is_clamped():
    candidate_embedding = np.array(
        [1.0, 0.0]
    )

    job_embedding = np.array(
        [-1.0, 0.0]
    )

    result = calculate_embedding_similarity(
        candidate_embedding,
        job_embedding
    )

    assert result == 0.0
