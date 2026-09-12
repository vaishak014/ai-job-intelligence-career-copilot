from app.candidate_strength_gap import (
    build_candidate_skill_map,
    extract_candidate_strengths,
    extract_market_strengths,
    extract_critical_gaps,
    extract_opportunity_gaps,
    identify_competitive_advantages,
    build_candidate_strength_gap_analysis
)


def test_build_candidate_skill_map():
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

    result = build_candidate_skill_map(
        candidate_skills
    )

    assert result["python"]["skill"] == "Python"
    assert result["sql"]["proficiency"] == "Advanced"


def test_extract_candidate_strengths():
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

    result = extract_candidate_strengths(
        candidate_skills
    )

    assert result[0]["skill"] == "SQL"
    assert result[1]["skill"] == "Python"
    assert result[2]["skill"] == "Git"

    assert result[0]["strength_score"] == 100.0


def test_extract_market_strengths():
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
            "demand_percentage": 27.27,
            "job_count": 3
        }
    ]

    result = extract_market_strengths(
        candidate_skills,
        market_skill_demand
    )

    assert len(result) == 2
    assert result[0]["skill"] == "SQL"
    assert result[0]["market_demand"] == 27.27
    assert result[0]["job_count"] == 3


def test_extract_critical_gaps():
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
            "skill": "Kotlin",
            "candidate_proficiency": "Missing",
            "priority_category": "Medium Priority",
            "priority_score": 36.36,
            "required_count": 2,
            "market_coverage": 18.18
        },
        {
            "skill": "Python",
            "candidate_proficiency": "Intermediate",
            "priority_category": "Low Priority",
            "priority_score": 10.0,
            "required_count": 1,
            "market_coverage": 18.18
        }
    ]

    result = extract_critical_gaps(
        skill_priorities
    )

    assert len(result) == 2
    assert result[0]["skill"] == "Git"
    assert result[1]["skill"] == "Kotlin"


def test_extract_opportunity_gaps():
    job_matches = [
        {
            "opportunity_type": "Semantic Opportunity",
            "missing_required": [
                "AWS",
                "Git"
            ]
        },
        {
            "opportunity_type": "Semantic Opportunity",
            "missing_required": [
                "Git"
            ]
        },
        {
            "opportunity_type": "Strong Match",
            "missing_required": [
                "Docker"
            ]
        }
    ]

    skill_priorities = [
        {
            "skill": "AWS",
            "candidate_proficiency": "Missing",
            "priority_score": 40.0,
            "required_count": 2,
            "market_coverage": 20.0
        },
        {
            "skill": "Git",
            "candidate_proficiency": "Missing",
            "priority_score": 50.0,
            "required_count": 3,
            "market_coverage": 30.0
        }
    ]

    result = extract_opportunity_gaps(
        job_matches,
        skill_priorities
    )

    assert len(result) == 2
    assert result[0]["skill"] == "Git"
    assert result[0]["semantic_jobs"] == 2
    assert result[1]["skill"] == "AWS"
    assert result[1]["semantic_jobs"] == 1


def test_identify_competitive_advantages():
    candidate_skills = [
        {
            "skill": "SQL",
            "proficiency": "Advanced"
        },
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        }
    ]

    market_skill_demand = [
        {
            "skill": "SQL",
            "demand_percentage": 27.27,
            "job_count": 3
        },
        {
            "skill": "Python",
            "demand_percentage": 18.18,
            "job_count": 2
        }
    ]

    result = identify_competitive_advantages(
        candidate_skills,
        market_skill_demand
    )

    assert len(result) == 1
    assert result[0]["skill"] == "SQL"
    assert result[0]["proficiency"] == "Advanced"


def test_build_candidate_strength_gap_analysis():
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
            "opportunity_type": "Semantic Opportunity",
            "missing_required": [
                "Git"
            ]
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
            "demand_percentage": 18.18,
            "job_count": 2
        },
        {
            "skill": "SQL",
            "demand_percentage": 27.27,
            "job_count": 3
        }
    ]

    result = build_candidate_strength_gap_analysis(
        candidate_skills,
        job_matches,
        skill_priorities,
        market_skill_demand
    )

    assert len(result["strengths"]) == 2
    assert len(result["market_strengths"]) == 2
    assert len(result["critical_gaps"]) == 1
    assert len(result["opportunity_gaps"]) == 1
    assert len(result["competitive_advantages"]) == 1

    assert result["strengths"][0]["skill"] == "SQL"
    assert result["critical_gaps"][0]["skill"] == "Git"
    assert result["opportunity_gaps"][0]["skill"] == "Git"
    assert (
        result["competitive_advantages"][0]["skill"]
        == "SQL"
    )
