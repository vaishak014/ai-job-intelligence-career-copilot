from app.skill_priority_engine import (
    calculate_skill_priority,
    generate_skill_priorities,
    get_priority_category
)


def test_missing_skill_with_high_market_demand_gets_high_priority():
    gap = {
        "skill": "React",
        "candidate_proficiency": "Missing",
        "gap_factor": 1.0,
        "required_count": 3,
        "preferred_count": 0,
        "opportunity_count": 3,
        "job_ids": [1, 2, 3],
        "job_titles": [
            "Frontend Developer",
            "Software Engineer",
            "Full Stack Developer"
        ]
    }

    score = calculate_skill_priority(
        gap,
        total_jobs=12,
        market_demand=25.0
    )

    assert score == 50.0
    assert get_priority_category(score) == "High Priority"


def test_beginner_skill_has_lower_priority_than_missing_skill():
    missing_gap = {
        "skill": "React",
        "candidate_proficiency": "Missing",
        "gap_factor": 1.0,
        "required_count": 3,
        "preferred_count": 0,
        "opportunity_count": 3
    }

    beginner_gap = {
        "skill": "React",
        "candidate_proficiency": "Beginner",
        "gap_factor": 0.75,
        "required_count": 3,
        "preferred_count": 0,
        "opportunity_count": 3
    }

    missing_score = calculate_skill_priority(
        missing_gap,
        12,
        25.0
    )

    beginner_score = calculate_skill_priority(
        beginner_gap,
        12,
        25.0
    )

    assert missing_score > beginner_score


def test_intermediate_skill_has_smaller_gap():
    gap = {
        "skill": "Python",
        "candidate_proficiency": "Intermediate",
        "gap_factor": 0.4,
        "required_count": 2,
        "preferred_count": 0,
        "opportunity_count": 2
    }

    score = calculate_skill_priority(
        gap,
        12,
        16.67
    )

    assert score == 13.34


def test_advanced_skill_has_zero_gap_factor():
    gap = {
        "skill": "Python",
        "candidate_proficiency": "Advanced",
        "gap_factor": 0.0,
        "required_count": 2,
        "preferred_count": 0,
        "opportunity_count": 2
    }

    score = calculate_skill_priority(
        gap,
        12,
        16.67
    )

    assert score == 0.0


def test_market_demand_is_used_for_priority():
    gaps = [
        {
            "skill": "React",
            "candidate_proficiency": "Missing",
            "gap_factor": 1.0,
            "required_count": 1,
            "preferred_count": 0,
            "opportunity_count": 1,
            "job_ids": [1],
            "job_titles": ["Frontend Developer"]
        },
        {
            "skill": "FastAPI",
            "candidate_proficiency": "Beginner",
            "gap_factor": 0.75,
            "required_count": 1,
            "preferred_count": 0,
            "opportunity_count": 1,
            "job_ids": [2],
            "job_titles": ["Backend Developer"]
        }
    ]

    demand = [
        {
            "skill": "React",
            "demand_percentage": 25.0
        },
        {
            "skill": "FastAPI",
            "demand_percentage": 8.33
        }
    ]

    results = generate_skill_priorities(
        gaps,
        12,
        demand
    )

    assert results[0]["skill"] == "React"
    assert results[0]["market_coverage"] == 25.0
    assert results[1]["skill"] == "FastAPI"
    assert results[1]["market_coverage"] == 8.33
