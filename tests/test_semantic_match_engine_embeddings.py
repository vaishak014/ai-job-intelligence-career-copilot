from unittest.mock import patch

from app.semantic_match_engine import (
    build_embedding_matches
)


def test_build_embedding_matches_ranks_by_combined_score():
    candidate_profile = {
        "education": "Computer Science",
        "experience_years": 0
    }

    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        }
    ]

    jobs = [
        {
            "job_id": 1,
            "title": "Job A",
            "company": "Company A"
        },
        {
            "job_id": 2,
            "title": "Job B",
            "company": "Company B"
        }
    ]

    job_matches = [
        {
            "job_id": 1,
            "title": "Job A",
            "company": "Company A",
            "overall_match": 80.0,
            "match_category": "Strong Match"
        },
        {
            "job_id": 2,
            "title": "Job B",
            "company": "Company B",
            "overall_match": 60.0,
            "match_category": "Moderate Match"
        }
    ]

    fake_candidate_embedding = "candidate_embedding"

    fake_job_embeddings = {
        1: "job_embedding_1",
        2: "job_embedding_2"
    }

    with patch(
        "app.semantic_match_engine.generate_candidate_embedding",
        return_value=fake_candidate_embedding
    ), patch(
        "app.semantic_match_engine.generate_job_embeddings",
        return_value=fake_job_embeddings
    ), patch(
        "app.semantic_match_engine.calculate_embedding_similarity",
        side_effect=lambda candidate, job: {
            "job_embedding_1": 20.0,
            "job_embedding_2": 80.0
        }[job]
    ):

        results = build_embedding_matches(
            candidate_profile,
            candidate_skills,
            job_matches,
            jobs
        )

    assert len(results) == 2

    assert results[0]["job_id"] == 2
    assert results[1]["job_id"] == 1

    assert results[0]["combined_match"] == 66.0
    assert results[1]["combined_match"] == 62.0


def test_build_embedding_matches_includes_semantic_signal():
    candidate_profile = {
        "education": "Computer Science",
        "experience_years": 0
    }

    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        }
    ]

    jobs = [
        {
            "job_id": 1,
            "title": "Job A",
            "company": "Company A"
        },
        {
            "job_id": 2,
            "title": "Job B",
            "company": "Company B"
        }
    ]

    job_matches = [
        {
            "job_id": 1,
            "title": "Job A",
            "company": "Company A",
            "overall_match": 25.0,
            "match_category": "Low Match"
        },
        {
            "job_id": 2,
            "title": "Job B",
            "company": "Company B",
            "overall_match": 80.0,
            "match_category": "Strong Match"
        }
    ]

    fake_candidate_embedding = "candidate_embedding"

    fake_job_embeddings = {
        1: "job_embedding_1",
        2: "job_embedding_2"
    }

    with patch(
        "app.semantic_match_engine.generate_candidate_embedding",
        return_value=fake_candidate_embedding
    ), patch(
        "app.semantic_match_engine.generate_job_embeddings",
        return_value=fake_job_embeddings
    ), patch(
        "app.semantic_match_engine.calculate_embedding_similarity",
        side_effect=lambda candidate, job: {
            "job_embedding_1": 60.0,
            "job_embedding_2": 50.0
        }[job]
    ):

        results = build_embedding_matches(
            candidate_profile,
            candidate_skills,
            job_matches,
            jobs
        )

    result_by_id = {
        result["job_id"]: result
        for result in results
    }

    assert (
        result_by_id[1]["semantic_signal"]
        == "Semantic Advantage"
    )

    assert (
        result_by_id[2]["semantic_signal"]
        == "Skill Advantage"
    )
