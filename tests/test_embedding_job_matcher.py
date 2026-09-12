import numpy as np

from app.embedding_job_matcher import (
    generate_candidate_embedding,
    generate_job_embedding,
    generate_job_embeddings
)


class MockModel:

    def encode(
        self,
        text,
        convert_to_numpy=True
    ):
        return np.array(
            [1.0, 2.0, 3.0]
        )


def test_generate_candidate_embedding():
    profile = {
        "education": "Computer Science",
        "experience_years": 0.0
    }

    skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Intermediate"
        }
    ]

    result = generate_candidate_embedding(
        profile,
        skills,
        MockModel()
    )

    assert result is not None
    assert result.shape == (3,)


def test_generate_job_embedding():
    job = {
        "job_id": 1,
        "title": "Python Developer",
        "company": "Company A",
        "description": "Python backend development",
        "source_criteria": [
            "Python programming",
            "SQL"
        ]
    }

    result = generate_job_embedding(
        job,
        MockModel()
    )

    assert result is not None
    assert result.shape == (3,)


def test_generate_job_embeddings():
    jobs = [
        {
            "job_id": 1,
            "title": "Python Developer",
            "company": "Company A",
            "description": "Python backend development",
            "source_criteria": [
                "Python"
            ]
        },
        {
            "job_id": 2,
            "title": "Data Analyst",
            "company": "Company B",
            "description": "Data analysis",
            "source_criteria": [
                "SQL"
            ]
        }
    ]

    result = generate_job_embeddings(
        jobs,
        MockModel()
    )

    assert len(result) == 2
    assert 1 in result
    assert 2 in result
    assert result[1].shape == (3,)
    assert result[2].shape == (3,)
