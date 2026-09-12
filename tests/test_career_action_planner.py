from app.career_action_planner import (
    get_action_type,
    build_action_text,
    create_career_action,
    build_career_action_plan
)


def test_get_action_type():
    assert get_action_type("Missing") == "Learn"
    assert get_action_type("Beginner") == "Improve"
    assert get_action_type("Intermediate") == "Strengthen"
    assert get_action_type("Advanced") == "Maintain"


def test_build_action_text():
    assert (
        build_action_text(
            "REST APIs",
            "Missing"
        )
        == "Learn REST APIs to increase job eligibility."
    )

    assert (
        build_action_text(
            "Python",
            "Intermediate"
        )
        == "Strengthen your Python proficiency for stronger job matches."
    )


def test_create_career_action():
    priority = {
        "skill": "REST APIs",
        "priority_category": "High Priority",
        "priority_score": 66.66,
        "candidate_proficiency": "Missing",
        "market_coverage": 33.33,
        "opportunity_count": 4,
        "required_count": 4,
        "preferred_count": 0,
        "job_ids": [1, 2, 3, 4],
        "job_titles": [
            "Python Developer",
            "Backend Developer"
        ]
    }

    result = create_career_action(priority)

    assert result["skill"] == "REST APIs"
    assert result["priority_category"] == "High Priority"
    assert result["candidate_proficiency"] == "Missing"
    assert result["action_type"] == "Learn"
    assert result["market_coverage"] == 33.33
    assert result["required_count"] == 4
    assert (
        result["action"]
        == "Learn REST APIs to increase job eligibility."
    )


def test_build_career_action_plan():
    priorities = [
        {
            "skill": "Git",
            "priority_category": "High Priority",
            "priority_score": 50.0,
            "candidate_proficiency": "Missing",
            "market_coverage": 25.0,
            "opportunity_count": 3,
            "required_count": 3,
            "preferred_count": 0
        },
        {
            "skill": "REST APIs",
            "priority_category": "High Priority",
            "priority_score": 66.66,
            "candidate_proficiency": "Missing",
            "market_coverage": 33.33,
            "opportunity_count": 4,
            "required_count": 4,
            "preferred_count": 0
        }
    ]

    result = build_career_action_plan(priorities)

    assert len(result) == 2
    assert result[0]["skill"] == "REST APIs"
    assert result[1]["skill"] == "Git"
