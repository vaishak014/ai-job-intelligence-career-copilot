import numpy as np

from app.embedding_ranker import (
    calculate_embedding_job_matches
)


def test_embedding_job_matches_are_ranked():
    candidate_embedding = np.array(
        [1.0, 0.0, 0.0]
    )

    jobs = [
        {
            "job_id": 1,
            "title": "Python Developer",
            "company": "Company A"
        },
        {
            "job_id": 2,
            "title": "Designer",
            "company": "Company B"
        }
    ]

    job_embeddings = {
        1: np.array(
            [1.0, 0.0, 0.0]
        ),
        2: np.array(
            [0.0, 1.0, 0.0]
        )
    }

    results = calculate_embedding_job_matches(
        candidate_embedding,
        jobs,
        job_embeddings
    )

    assert len(results) == 2

    assert results[0]["job_id"] == 1

    assert (
        results[0]["embedding_similarity"]
        == 100.0
    )

    assert (
        results[1]["embedding_similarity"]
        == 0.0
    )


def test_embedding_job_matches_empty_candidate():
    jobs = [
        {
            "job_id": 1,
            "title": "Python Developer",
            "company": "Company A"
        }
    ]

    job_embeddings = {
        1: np.array(
            [1.0, 0.0, 0.0]
        )
    }

    results = calculate_embedding_job_matches(
        None,
        jobs,
        job_embeddings
    )

    assert len(results) == 1
    assert (
        results[0]["embedding_similarity"]
        == 0.0
    )


def test_embedding_job_matches_missing_job_embedding():
    candidate_embedding = np.array(
        [1.0, 0.0, 0.0]
    )

    jobs = [
        {
            "job_id": 1,
            "title": "Python Developer",
            "company": "Company A"
        }
    ]

    results = calculate_embedding_job_matches(
        candidate_embedding,
        jobs,
        {}
    )

    assert len(results) == 1
    assert (
        results[0]["embedding_similarity"]
        == 0.0
    )
