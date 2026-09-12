from app.semantic_match_engine import (
    calculate_combined_match,
    classify_semantic_signal,
    classify_opportunity_type,
    build_embedding_matches
)


def test_calculate_combined_match():
    result = calculate_combined_match(
        80,
        60
    )

    assert result == 74.0


def test_calculate_combined_match_caps_at_100():
    result = calculate_combined_match(
        100,
        120
    )

    assert result == 100.0


def test_classify_semantic_signal():
    assert classify_semantic_signal(
        40,
        70
    ) == "Semantic Advantage"

    assert classify_semantic_signal(
        70,
        40
    ) == "Skill Advantage"

    assert classify_semantic_signal(
        60,
        65
    ) == "Balanced"


def test_classify_opportunity_type():
    assert classify_opportunity_type(
        50,
        60
    ) == "Strong Match"

    assert classify_opportunity_type(
        53.33,
        63.42
    ) == "Strong Match"

    assert classify_opportunity_type(
        10,
        40
    ) == "Semantic Opportunity"

    assert classify_opportunity_type(
        50,
        30
    ) == "Skill Match"

    assert classify_opportunity_type(
        10,
        20
    ) == "Low Relevance"


def test_build_embedding_matches():
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
            "overall_match": 60.0,
            "match_category": "Moderate Match",
            "matched_required": [],
            "missing_required": [],
            "matched_preferred": [],
            "missing_preferred": []
        },
        {
            "job_id": 2,
            "title": "Job B",
            "company": "Company B",
            "overall_match": 80.0,
            "match_category": "Strong Match",
            "matched_required": [],
            "missing_required": [],
            "matched_preferred": [],
            "missing_preferred": []
        }
    ]

    from unittest.mock import patch

    fake_candidate_embedding = "candidate_embedding"

    fake_job_embeddings = {
        1: "job_embedding_1",
        2: "job_embedding_2"
    }

    def fake_similarity(
        candidate_embedding,
        job_embedding
    ):
        if job_embedding == "job_embedding_1":
            return 70.0

        return 50.0

    with patch(
        "app.semantic_match_engine."
        "generate_candidate_embedding",
        return_value=fake_candidate_embedding
    ), patch(
        "app.semantic_match_engine."
        "generate_job_embeddings",
        return_value=fake_job_embeddings
    ), patch(
        "app.semantic_match_engine."
        "calculate_embedding_similarity",
        side_effect=fake_similarity
    ):

        results = build_embedding_matches(
            candidate_profile,
            candidate_skills,
            job_matches,
            jobs,
            model="fake_model"
        )

    assert len(results) == 2

    assert results[0]["job_id"] == 2
    assert results[1]["job_id"] == 1

    assert results[0]["skill_match_score"] == 80.0
    assert results[0]["semantic_similarity"] == 50.0
    assert results[0]["combined_match"] == 71.0

    assert results[1]["skill_match_score"] == 60.0
    assert results[1]["semantic_similarity"] == 70.0
    assert results[1]["combined_match"] == 63.0


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
            "match_category": "Low Match",
            "matched_required": [],
            "missing_required": [],
            "matched_preferred": [],
            "missing_preferred": []
        },
        {
            "job_id": 2,
            "title": "Job B",
            "company": "Company B",
            "overall_match": 80.0,
            "match_category": "Strong Match",
            "matched_required": [],
            "missing_required": [],
            "matched_preferred": [],
            "missing_preferred": []
        }
    ]

    from unittest.mock import patch

    fake_candidate_embedding = "candidate_embedding"

    fake_job_embeddings = {
        1: "job_embedding_1",
        2: "job_embedding_2"
    }

    def fake_similarity(
        candidate_embedding,
        job_embedding
    ):
        if job_embedding == "job_embedding_1":
            return 60.0

        return 50.0

    with patch(
        "app.semantic_match_engine."
        "generate_candidate_embedding",
        return_value=fake_candidate_embedding
    ), patch(
        "app.semantic_match_engine."
        "generate_job_embeddings",
        return_value=fake_job_embeddings
    ), patch(
        "app.semantic_match_engine."
        "calculate_embedding_similarity",
        side_effect=fake_similarity
    ):

        results = build_embedding_matches(
            candidate_profile,
            candidate_skills,
            job_matches,
            jobs,
            model="fake_model"
        )

    semantic_job = next(
        item
        for item in results
        if item["job_id"] == 1
    )

    skill_job = next(
        item
        for item in results
        if item["job_id"] == 2
    )

    assert semantic_job["semantic_signal"] == (
        "Semantic Advantage"
    )

    assert skill_job["semantic_signal"] == (
        "Skill Advantage"
    )


def test_build_embedding_matches_includes_opportunity_type():
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
            "title": "Python Developer",
            "company": "Test Company"
        }
    ]

    job_matches = [
        {
            "job_id": 1,
            "title": "Python Developer",
            "company": "Test Company",
            "overall_match": 10.0,
            "match_category": "Low Match",
            "matched_required": [],
            "missing_required": [],
            "matched_preferred": [],
            "missing_preferred": []
        }
    ]

    from unittest.mock import patch

    fake_candidate_embedding = "candidate_embedding"

    fake_job_embeddings = {
        1: "job_embedding"
    }

    with patch(
        "app.semantic_match_engine."
        "generate_candidate_embedding",
        return_value=fake_candidate_embedding
    ), patch(
        "app.semantic_match_engine."
        "generate_job_embeddings",
        return_value=fake_job_embeddings
    ), patch(
        "app.semantic_match_engine."
        "calculate_embedding_similarity",
        return_value=40.0
    ):

        results = build_embedding_matches(
            candidate_profile,
            candidate_skills,
            job_matches,
            jobs,
            model="fake_model"
        )

    assert len(results) == 1

    assert results[0]["opportunity_type"] == (
        "Semantic Opportunity"
    )
