from app.interview_intelligence import (
    build_interview_intelligence
)


def test_build_interview_intelligence():

    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Intermediate"
        }
    ]

    job_match = {
        "job_id": 1,
        "title": "Python Developer",
        "company": "Test Company",
        "combined_match": 56.0,
        "skill_details": [
            {
                "skill": "Python",
                "importance": "Required",
                "status": "Matched"
            },
            {
                "skill": "SQL",
                "importance": "Required",
                "status": "Matched"
            },
            {
                "skill": "PySpark",
                "importance": "Required",
                "status": "Missing"
            }
        ]
    }

    result = build_interview_intelligence(
        candidate_skills,
        job_match
    )

    assert result is not None
    assert result["job_title"] == "Python Developer"
    assert result["company"] == "Test Company"
    assert result["interview_readiness"] == "Moderate"

    assert "Python" in result["matched_required"]
    assert "SQL" in result["matched_required"]
    assert "PySpark" in result["missing_required"]

    assert len(result["interview_focus"]) == 3
    assert len(result["technical_topics"]) == 3
    assert len(result["project_defense_topics"]) == 3


def test_missing_job_returns_none():

    result = build_interview_intelligence(
        [],
        None
    )

    assert result is None


def test_low_match_is_low_readiness():

    candidate_skills = []

    job_match = {
        "job_id": 2,
        "title": "Software Engineer",
        "company": "Test Company",
        "combined_match": 20.0,
        "skill_details": [
            {
                "skill": "Python",
                "importance": "Required",
                "status": "Missing"
            }
        ]
    }

    result = build_interview_intelligence(
        candidate_skills,
        job_match
    )

    assert result["interview_readiness"] == "Low"
    assert "Python" in result["missing_required"]
