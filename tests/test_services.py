from app.services import (
    get_job_by_id,
    get_candidate_by_id,
    get_candidate_skill_data,
    get_candidate_match_data,
    get_candidate_intelligence_data,
    get_candidate_recommendation_data,
    get_candidate_skill_gap_data,
    get_application_statistics_data
)


def test_get_existing_job():
    job = get_job_by_id(1)

    assert job is not None
    assert job["job_id"] == 1
    assert job["title"] == "Python Backend Developer"


def test_get_non_existing_job():
    job = get_job_by_id(999)

    assert job is None


def test_get_existing_candidate():
    candidate = get_candidate_by_id(1)

    assert candidate is not None
    assert candidate["candidate_id"] == 1
    assert candidate["education"] == "Computer Science"


def test_get_non_existing_candidate():
    candidate = get_candidate_by_id(999)

    assert candidate is None


def test_get_candidate_skills():
    skills = get_candidate_skill_data(1)

    assert skills is not None
    assert len(skills) > 0

    skill_names = [
        skill["skill"]
        for skill in skills
    ]

    assert "Python" in skill_names
    assert "SQL" in skill_names


def test_get_candidate_matches():
    matches = get_candidate_match_data(1)

    assert matches is not None
    assert len(matches) >= 3

    matches_by_job_id = {
        match["job_id"]: match
        for match in matches
    }

    assert 1 in matches_by_job_id
    assert 2 in matches_by_job_id
    assert 3 in matches_by_job_id

    data_analyst_match = matches_by_job_id[2]

    assert data_analyst_match["title"] == "Data Analyst"
    assert float(
        data_analyst_match["overall_match"]
    ) == 80.0


def test_get_candidate_intelligence():
    intelligence = get_candidate_intelligence_data(1)

    assert intelligence is not None

    assert "profile" in intelligence
    assert "candidate_skills" in intelligence
    assert "job_matches" in intelligence
    assert "recommendations" in intelligence
    assert "skill_gaps" in intelligence
    assert "skill_priorities" in intelligence
    assert "market_skill_demand" in intelligence


def test_get_candidate_recommendations():
    recommendations = get_candidate_recommendation_data(1)

    assert recommendations is not None
    assert len(recommendations) >= 3

    recommendations_by_job_id = {
        recommendation["job_id"]: recommendation
        for recommendation in recommendations
    }

    assert 1 in recommendations_by_job_id
    assert 2 in recommendations_by_job_id
    assert 3 in recommendations_by_job_id

    data_analyst_recommendation = (
        recommendations_by_job_id[2]
    )

    assert (
        data_analyst_recommendation["title"]
        == "Data Analyst"
    )

    assert (
        data_analyst_recommendation["recommendation"]
        == "Recommended"
    )


def test_get_candidate_skill_gaps():
    skill_gap_data = get_candidate_skill_gap_data(1)

    assert skill_gap_data is not None

    assert "skill_gaps" in skill_gap_data
    assert "skill_priorities" in skill_gap_data

    assert len(skill_gap_data["skill_gaps"]) > 0
    assert len(skill_gap_data["skill_priorities"]) > 0


def test_application_statistics():
    statistics = get_application_statistics_data()

    assert "not_applied" in statistics
    assert "applied" in statistics
    assert "interview" in statistics
    assert "rejected" in statistics
    assert "offer" in statistics

    assert statistics["interview"] == 2
