from app.ai_career_copilot import (
    build_copilot_context
)


def sample_intelligence():
    return {
        "profile": {
            "name": "Candidate",
            "education": "Computer Science",
            "experience_years": 0.0
        },

        "candidate_skills": [
            {
                "skill": "Python",
                "proficiency": "Intermediate"
            },
            {
                "skill": "SQL",
                "proficiency": "Intermediate"
            }
        ],

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

        "candidate_strength_gap": {
            "strengths": [
                {
                    "skill": "Python",
                    "proficiency": "Intermediate"
                }
            ],
            "market_strengths": [
                {
                    "skill": "Python"
                }
            ],
            "critical_gaps": [
                {
                    "skill": "Git",
                    "priority_category": "High Priority"
                }
            ],
            "competitive_advantages": []
        },

        "career_readiness_explanation": {
            "summary": {
                "readiness_score": 47.87
            },
            "what_is_helping": [
                {
                    "factor": "Core Skills"
                }
            ],
            "what_is_holding_back": [
                {
                    "factor": "Job Fit"
                }
            ],
            "priority_actions": [
                {
                    "skill": "Git"
                }
            ],
            "realistic_opportunities": [
                {
                    "title": "Python Developer"
                }
            ],
            "career_direction": "Build targeted skills."
        },

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

        "career_action_plan": [
            {
                "skill": "Git"
            }
        ],

        "skill_priorities": [
            {
                "skill": "Git"
            }
        ],

        "job_matches": [
            {
                "job_id": 1,
                "title": "Python Developer"
            }
        ],

        "market_skill_demand": [
            {
                "skill": "Git",
                "demand_percentage": 27.27
            }
        ]
    }


def test_build_copilot_context():
    result = build_copilot_context(
        sample_intelligence()
    )

    assert result is not None

    assert (
        result["candidate"]["name"]
        == "Candidate"
    )

    assert (
        result["readiness"]["score"]
        == 47.87
    )

    assert (
        result["candidate_segment"]["type"]
        == "Semantic-Potential Candidate"
    )

    assert (
        result["current_skills"][0]["skill"]
        == "Python"
    )

    assert (
        result["critical_gaps"][0]["skill"]
        == "Git"
    )

    assert (
        result["career_strategy"][
            "strongest_skill"
        ]
        == "Python"
    )

    assert (
        result["top_job_matches"][0]["title"]
        == "Python Developer"
    )


def test_copilot_context_limits_lists():
    intelligence = sample_intelligence()

    intelligence["job_matches"] = [
        {"job_id": number}
        for number in range(10)
    ]

    intelligence["skill_priorities"] = [
        {"skill": str(number)}
        for number in range(10)
    ]

    intelligence["market_skill_demand"] = [
        {"skill": str(number)}
        for number in range(20)
    ]

    result = build_copilot_context(
        intelligence
    )

    assert len(
        result["top_job_matches"]
    ) == 5

    assert len(
        result["skill_priorities"]
    ) == 5

    assert len(
        result["market_skill_demand"]
    ) == 10


def test_copilot_context_handles_none():
    result = build_copilot_context(
        None
    )

    assert result is None
