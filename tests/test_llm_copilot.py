from app.llm_copilot import (
    build_system_prompt,
    build_candidate_context_prompt,
    build_copilot_prompt
)


def sample_context():
    return {
        "candidate": {
            "name": "Candidate",
            "education": "Computer Science",
            "experience_years": 0.0
        },
        "current_skills": [
            {
                "skill": "Python",
                "proficiency": "Intermediate"
            },
            {
                "skill": "SQL",
                "proficiency": "Intermediate"
            }
        ],
        "readiness": {
            "score": 47.87,
            "level": "Developing",
            "skill_strength": 75.0,
            "job_fit": 26.5,
            "market_alignment": 36.36,
            "semantic_opportunities": 4
        },
        "candidate_segment": {
            "type": "Semantic-Potential Candidate",
            "reason": "Multiple semantically relevant opportunities."
        },
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
        "competitive_advantages": [],
        "career_strategy": {
            "strongest_skill": "Python",
            "best_job_match": {
                "title": "Python Developer",
                "company": "Cognizant"
            },
            "top_improvements": [
                {
                    "skill": "Git"
                }
            ],
            "strategy_direction": (
                "Prioritize Python opportunities."
            )
        },
        "career_action_plan": [
            {
                "skill": "Git",
                "action_type": "Learn"
            }
        ],
        "skill_priorities": [
            {
                "skill": "Git",
                "priority_category": "High Priority"
            }
        ],
        "top_job_matches": [
            {
                "title": "Python Developer",
                "company": "Cognizant",
                "combined_match": 56.36
            }
        ],
        "market_skill_demand": [
            {
                "skill": "Git",
                "demand_percentage": 27.27
            }
        ],
        "readiness_explanation": {
            "career_direction": (
                "Build Python opportunities while "
                "closing skill gaps."
            )
        }
    }


def test_build_system_prompt():
    result = build_system_prompt()

    assert result is not None
    assert "AI Career Copilot" in result
    assert "Do not invent" in result
    assert "candidate" in result.lower()


def test_build_candidate_context_prompt():
    result = build_candidate_context_prompt(
        sample_context()
    )

    assert result is not None
    assert "Computer Science" in result
    assert "Python" in result
    assert "Git" in result
    assert "47.87" in result
    assert "Cognizant" in result


def test_build_candidate_context_prompt_handles_none():
    result = build_candidate_context_prompt(None)

    assert result == ""


def test_build_copilot_prompt():
    result = build_copilot_prompt(
        sample_context()
    )

    assert result is not None
    assert "system_prompt" in result
    assert "candidate_prompt" in result
    assert "AI Career Copilot" in result["system_prompt"]
    assert "Python" in result["candidate_prompt"]


def test_build_copilot_prompt_handles_none():
    result = build_copilot_prompt(None)

    assert result is None
