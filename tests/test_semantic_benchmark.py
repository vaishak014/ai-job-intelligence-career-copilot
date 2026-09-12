from app.semantic_benchmark import (
    benchmark_semantic_methods
)


def test_benchmark_returns_semantic_scores():
    results = benchmark_semantic_methods(
        1,
        "Software Engineering"
    )

    assert isinstance(results, list)

    if results:
        first = results[0]

        assert "job_id" in first
        assert "title" in first
        assert "company" in first
        assert "tfidf_similarity" in first
        assert "embedding_similarity" in first

        assert (
            0.0
            <= first["tfidf_similarity"]
            <= 100.0
        )

        assert (
            0.0
            <= first["embedding_similarity"]
            <= 100.0
        )
