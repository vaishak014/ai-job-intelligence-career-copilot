from app.career_dashboard import (
    build_career_dashboard
)


def sample_intelligence():
    return {
        "profile": {
            "name": "Candidate",
            "education": "Computer Science",
            "experience_years": 0.0
        },

        "candidate_readiness": {
            "readiness_score": 47.87,
            "readiness_level": "Developing",
            "skill_strength": 75.0,
            "job_fit": 26.5,
            "market_alignment": 36.36,
            "semantic_opportunity_count": 4
        },

        "candidate_segmentation": {
            "profile_type": "Semantic-Potential Candidate",
            "reason": "Semantic relevance exists."
        },

        "career_readiness_explanation": {
            "summary": {
                "readiness_score": 47.87,
                "readiness_level": "Developing"
            },
            "what_is_helping": [
                {
                    "factor": "Core Skills",
                    "details": "Python and SQL."
                }
            ],
            "what_is_holding_back": [
                {
                    "factor": "Job Fit",
                    "details": "Limited direct alignment."
                }
            ],
            "priority_actions": [
                {
                    "rank": 1,
                    "skill": "Git"
                }
            ],
            "realistic_opportunities": [
                {
                    "job_id": 1,
                    "title": "Python Developer"
                }
            ],
            "career_direction": "Build targeted skills."
        },

        "job_matches": [
            {
                "job_id": 1,
                "title": "Python Developer"
            }
        ],

        "skill_priorities": [
            {
                "skill": "Git"
            }
        ],

        "career_action_plan": [
            {
                "skill": "Git"
            }
        ],

        "career_strategy": {
            "strongest_skill": "Python",
            "best_job_match": {
                "title": "Python Developer"
            },
            "top_improvements": [
                {
                    "skill": "Git"
                }
            ],
            "strategy_direction": "Focus on Python roles."
        },

        "candidate_strength_gap": {
            "strengths": [
                {
                    "skill": "Python"
                }
            ],
            "market_strengths": [
                {
                    "skill": "Python"
                }
            ],
            "critical_gaps": [
                {
                    "skill": "Git"
                }
            ],
            "competitive_advantages": []
        },

        "market_skill_demand": [
            {
                "skill": "Git",
                "demand_percentage": 27.27
            }
        ]
    }


def test_build_career_dashboard():
    result = build_career_dashboard(
        sample_intelligence()
    )

    assert result is not None

    assert result["candidate"]["name"] == "Candidate"

    assert (
        result["readiness"]["score"]
        == 47.87
    )

    assert (
        result["readiness"]["level"]
        == "Developing"
    )

    assert (
        result["candidate_segment"]["type"]
        == "Semantic-Potential Candidate"
    )

    assert (
        result["readiness_explanation"][
            "career_direction"
        ]
        == "Build targeted skills."
    )

    assert (
        result["top_job_matches"][0]["title"]
        == "Python Developer"
    )

    assert (
        result["top_skill_priorities"][0]["skill"]
        == "Git"
    )

    assert (
        result["career_strategy"][
            "strongest_skill"
        ]
        == "Python"
    )

    assert (
        result["critical_gaps"][0]["skill"]
        == "Git"
    )


def test_dashboard_limits_long_lists():
    intelligence = sample_intelligence()

    intelligence["job_matches"] = [
        {"job_id": number}
        for number in range(10)
    ]

    intelligence["skill_priorities"] = [
        {"skill": str(number)}
        for number in range(10)
    ]

    result = build_career_dashboard(
        intelligence
    )

    assert len(
        result["top_job_matches"]
    ) == 5

    assert len(
        result["top_skill_priorities"]
    ) == 5


def test_dashboard_handles_none():
    result = build_career_dashboard(
        None
    )

    assert result is None
