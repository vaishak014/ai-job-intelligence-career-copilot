from app.career_explainer import (
    explain_skill_priority,
    explain_skill_priorities,
    explain_job_match,
    explain_job_matches
)


def test_explain_skill_priority():
    priority = {
        "skill": "Python",
        "candidate_proficiency": "Intermediate",
        "market_coverage": 40.0,
        "opportunity_count": 4,
        "required_count": 3,
        "preferred_count": 1,
        "priority_category": "High Priority",
        "priority_score": 80.0
    }

    result = explain_skill_priority(
        priority,
        10
    )

    assert result["skill"] == "Python"
    assert result["priority_category"] == "High Priority"
    assert result["priority_score"] == 80.0
    assert result["candidate_proficiency"] == "Intermediate"
    assert result["market_coverage"] == 40.0
    assert result["opportunity_count"] == 4
    assert result["required_count"] == 3
    assert result["preferred_count"] == 1
    assert len(result["explanation"]) == 4


def test_explain_skill_priorities():
    priorities = [
        {
            "skill": "Python",
            "candidate_proficiency": "Intermediate",
            "market_coverage": 40.0,
            "opportunity_count": 4,
            "required_count": 3,
            "preferred_count": 1,
            "priority_category": "High Priority",
            "priority_score": 80.0
        },
        {
            "skill": "SQL",
            "candidate_proficiency": "Beginner",
            "market_coverage": 30.0,
            "opportunity_count": 3,
            "required_count": 2,
            "preferred_count": 1,
            "priority_category": "Medium Priority",
            "priority_score": 50.0
        }
    ]

    results = explain_skill_priorities(
        priorities,
        10
    )

    assert len(results) == 2
    assert results[0]["skill"] == "Python"
    assert results[1]["skill"] == "SQL"


def test_explain_job_match():
    job_match = {
        "job_id": 1,
        "title": "Python Developer",
        "company": "Cognizant",
        "overall_match": 53.33,
        "skill_match_score": 53.33,
        "semantic_similarity": 63.42,
        "combined_match": 56.36,
        "semantic_signal": "Balanced",
        "match_category": "Weak Match",
        "matched_required": [
            "Python",
            "SQL"
        ],
        "missing_required": [
            "PySpark"
        ],
        "matched_preferred": [],
        "missing_preferred": []
    }

    result = explain_job_match(
        job_match
    )

    assert result["job_id"] == 1
    assert result["title"] == "Python Developer"
    assert result["company"] == "Cognizant"
    assert result["skill_match_score"] == 53.33
    assert result["semantic_similarity"] == 63.42
    assert result["combined_match"] == 56.36
    assert result["semantic_signal"] == "Balanced"
    assert result["match_category"] == "Weak Match"

    assert (
        "✓ Python - Required skill matched"
        in result["explanation"]
    )

    assert (
        "✓ SQL - Required skill matched"
        in result["explanation"]
    )

    assert (
        "✗ PySpark - Required skill missing"
        in result["explanation"]
    )


def test_explain_job_match_preserves_semantic_advantage():
    job_match = {
        "job_id": 2,
        "title": "Software Engineer",
        "company": "SmartJoules",
        "overall_match": 26.67,
        "skill_match_score": 26.67,
        "semantic_similarity": 56.65,
        "combined_match": 35.66,
        "semantic_signal": "Semantic Advantage",
        "match_category": "Low Match",
        "matched_required": [
            "Python"
        ],
        "missing_required": [
            "AWS",
            "Time-Series Databases"
        ],
        "matched_preferred": [],
        "missing_preferred": []
    }

    result = explain_job_match(
        job_match
    )

    assert result["semantic_signal"] == (
        "Semantic Advantage"
    )


def test_explain_job_matches():
    job_matches = [
        {
            "job_id": 1,
            "title": "Python Developer",
            "company": "Cognizant",
            "overall_match": 53.33,
            "skill_match_score": 53.33,
            "semantic_similarity": 63.42,
            "combined_match": 56.36,
            "semantic_signal": "Balanced",
            "match_category": "Weak Match",
            "matched_required": [
                "Python"
            ],
            "missing_required": [
                "PySpark"
            ],
            "matched_preferred": [],
            "missing_preferred": []
        },
        {
            "job_id": 2,
            "title": "Software Engineer",
            "company": "SmartJoules",
            "overall_match": 26.67,
            "skill_match_score": 26.67,
            "semantic_similarity": 56.65,
            "combined_match": 35.66,
            "semantic_signal": "Semantic Advantage",
            "match_category": "Low Match",
            "matched_required": [
                "Python"
            ],
            "missing_required": [
                "AWS"
            ],
            "matched_preferred": [],
            "missing_preferred": []
        }
    ]

    results = explain_job_matches(
        job_matches
    )

    assert len(results) == 2
    assert results[0]["semantic_signal"] == "Balanced"
    assert results[1]["semantic_signal"] == (
        "Semantic Advantage"
    )


def test_explain_job_match_preserves_opportunity_type():
    job_match = {
        "job_id": 3,
        "title": "Software Engineer",
        "company": "KODEVEX Technologies",
        "overall_match": 0.0,
        "skill_match_score": 0.0,
        "semantic_similarity": 40.02,
        "combined_match": 12.01,
        "semantic_signal": "Semantic Advantage",
        "opportunity_type": "Semantic Opportunity",
        "match_category": "Low Match",
        "matched_required": [],
        "missing_required": [],
        "matched_preferred": [],
        "missing_preferred": []
    }

    result = explain_job_match(
        job_match
    )

    assert result["opportunity_type"] == (
        "Semantic Opportunity"
    )
