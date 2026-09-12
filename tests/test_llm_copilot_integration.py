from app.llm_copilot import (
    build_copilot_prompt
)


def test_llm_copilot_prompt_contains_candidate_data():
    context = {
        "candidate": {
            "name": "Candidate",
            "education": "Computer Science",
            "experience_years": 0.0
        },
        "current_skills": [
            {
                "skill": "Python",
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
            "reason": "Semantic relevance exists."
        },
        "strengths": [
            {
                "skill": "Python"
            }
        ],
        "market_strengths": [],
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
            "top_improvements": [],
            "strategy_direction": "Target Python roles."
        },
        "career_action_plan": [],
        "skill_priorities": [],
        "top_job_matches": [
            {
                "title": "Python Developer",
                "company": "Cognizant",
                "combined_match": 56.36
            }
        ],
        "market_skill_demand": [],
        "readiness_explanation": {}
    }

    result = build_copilot_prompt(context)

    assert result is not None
    assert "system_prompt" in result
    assert "candidate_prompt" in result

    assert "Python" in result["candidate_prompt"]
    assert "Git" in result["candidate_prompt"]
    assert "47.87" in result["candidate_prompt"]
    assert "Cognizant" in result["candidate_prompt"]


def test_llm_copilot_prompt_handles_none():
    result = build_copilot_prompt(None)

    assert result is None
