from app.candidate_readiness import (
    get_readiness_level,
    calculate_skill_strength,
    extract_strongest_skills,
    extract_market_relevant_skills,
    extract_major_blockers,
    calculate_job_fit_score,
    calculate_market_alignment,
    count_semantic_opportunities,
    calculate_readiness_score,
    build_candidate_readiness_profile
)


def test_get_readiness_level():
    assert get_readiness_level(80) == "Job Ready"
    assert get_readiness_level(65) == "Nearly Job Ready"
    assert get_readiness_level(50) == "Developing"
    assert get_readiness_level(30) == "Foundation Stage"


def test_calculate_skill_strength():
    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Advanced"
        }
    ]

    result = calculate_skill_strength(
        candidate_skills
    )

    assert result == 90.0


def test_calculate_skill_strength_empty():
    assert calculate_skill_strength([]) == 0.0


def test_extract_strongest_skills():
    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Advanced"
        },
        {
            "skill": "Git",
            "proficiency": "Beginner"
        }
    ]

    result = extract_strongest_skills(
        candidate_skills
    )

    assert result[0]["skill"] == "SQL"
    assert result[1]["skill"] == "Python"
    assert result[2]["skill"] == "Git"


def test_extract_market_relevant_skills():
    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Advanced"
        },
        {
            "skill": "Java",
            "proficiency": "Beginner"
        }
    ]

    market_skill_demand = [
        {
            "skill": "Python",
            "demand": 30.0,
            "jobs": 3
        },
        {
            "skill": "SQL",
            "demand": 50.0,
            "jobs": 5
        }
    ]

    result = extract_market_relevant_skills(
        candidate_skills,
        market_skill_demand
    )

    assert len(result) == 2
    assert result[0]["skill"] == "SQL"
    assert result[1]["skill"] == "Python"


def test_extract_major_blockers():
    skill_priorities = [
        {
            "skill": "Git",
            "candidate_proficiency": "Missing",
            "priority_category": "High Priority",
            "priority_score": 54.54,
            "required_count": 3,
            "market_coverage": 27.27
        },
        {
            "skill": "Python",
            "candidate_proficiency": "Intermediate",
            "priority_category": "Low Priority",
            "priority_score": 10.0,
            "required_count": 1,
            "market_coverage": 18.18
        },
        {
            "skill": "REST APIs",
            "candidate_proficiency": "Missing",
            "priority_category": "High Priority",
            "priority_score": 50.0,
            "required_count": 2,
            "market_coverage": 20.0
        }
    ]

    result = extract_major_blockers(
        skill_priorities
    )

    assert len(result) == 2
    assert result[0]["skill"] == "Git"
    assert result[1]["skill"] == "REST APIs"


def test_calculate_job_fit_score():
    job_matches = [
        {
            "combined_match": 60.0
        },
        {
            "combined_match": 40.0
        },
        {
            "combined_match": 20.0
        }
    ]

    result = calculate_job_fit_score(
        job_matches
    )

    assert result == 40.0


def test_calculate_job_fit_score_empty():
    assert calculate_job_fit_score([]) == 0.0


def test_calculate_market_alignment():
    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Advanced"
        }
    ]

    market_skill_demand = [
        {
            "skill": "Python",
            "demand": 18.18,
            "jobs": 2
        },
        {
            "skill": "SQL",
            "demand": 18.18,
            "jobs": 2
        }
    ]

    result = calculate_market_alignment(
        candidate_skills,
        market_skill_demand
    )

    assert result == 36.36


def test_count_semantic_opportunities():
    job_matches = [
        {
            "opportunity_type": "Semantic Opportunity"
        },
        {
            "opportunity_type": "Strong Match"
        },
        {
            "opportunity_type": "Semantic Opportunity"
        }
    ]

    result = count_semantic_opportunities(
        job_matches
    )

    assert result == 2


def test_calculate_readiness_score():
    result = calculate_readiness_score(
        80.0,
        60.0,
        40.0
    )

    assert result == 64.0


def test_build_candidate_readiness_profile():
    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Advanced"
        }
    ]

    job_matches = [
        {
            "combined_match": 60.0,
            "opportunity_type": "Strong Match"
        },
        {
            "combined_match": 40.0,
            "opportunity_type": "Semantic Opportunity"
        }
    ]

    skill_priorities = [
        {
            "skill": "Git",
            "candidate_proficiency": "Missing",
            "priority_category": "High Priority",
            "priority_score": 54.54,
            "required_count": 3,
            "market_coverage": 27.27
        }
    ]

    market_skill_demand = [
        {
            "skill": "Python",
            "demand": 18.18,
            "jobs": 2
        },
        {
            "skill": "SQL",
            "demand": 18.18,
            "jobs": 2
        }
    ]

    result = build_candidate_readiness_profile(
        candidate_skills,
        job_matches,
        skill_priorities,
        market_skill_demand
    )

    assert result["skill_strength"] == 90.0
    assert result["job_fit"] == 50.0
    assert result["market_alignment"] == 36.36

    expected_score = round(
        90.0 * 0.40
        + 50.0 * 0.40
        + 36.36 * 0.20,
        2
    )

    assert result["readiness_score"] == expected_score
    assert result["readiness_level"] == "Nearly Job Ready"

    assert result["strongest_skills"][0]["skill"] == "SQL"

    assert (
        result["market_relevant_skills"][0]["skill"]
        == "Python"
        or
        result["market_relevant_skills"][0]["skill"]
        == "SQL"
    )

    assert result["major_blockers"][0]["skill"] == "Git"

    assert result["semantic_opportunity_count"] == 1


def test_calculate_market_alignment_with_production_fields():
    candidate_skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Advanced"
        }
    ]

    market_skill_demand = [
        {
            "skill": "Python",
            "demand_percentage": 18.18,
            "job_count": 2
        },
        {
            "skill": "SQL",
            "demand_percentage": 18.18,
            "job_count": 2
        }
    ]

    result = calculate_market_alignment(
        candidate_skills,
        market_skill_demand
    )

    assert result == 36.36
