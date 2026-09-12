from app.career_advice_engine import (
    generate_readiness_advice,
    generate_strength_advice,
    generate_gap_advice,
    generate_market_advice,
    generate_job_search_advice,
    generate_learning_plan,
    generate_application_strategy,
    build_career_advice
)


def sample_context():
    return {
        "readiness": {
            "score": 47.87,
            "level": "Developing",
            "market_alignment": 36.36
        },

        "strengths": [
            {
                "skill": "Python",
                "proficiency": "Intermediate"
            },
            {
                "skill": "SQL",
                "proficiency": "Intermediate"
            }
        ],

        "market_strengths": [
            {
                "skill": "Python"
            },
            {
                "skill": "SQL"
            }
        ],

        "critical_gaps": [
            {
                "skill": "Git",
                "priority_category": "High Priority",
                "required_count": 3
            },
            {
                "skill": "REST APIs",
                "priority_category": "High Priority",
                "required_count": 3
            }
        ],

        "top_job_matches": [
            {
                "title": "Python Developer",
                "company": "Cognizant",
                "combined_match": 56.36
            }
        ],

        "readiness_explanation": {
            "realistic_opportunities": [
                {
                    "title": "Python Developer",
                    "opportunity_type": "Strong Match"
                },
                {
                    "title": "Software Engineer",
                    "opportunity_type": "Semantic Opportunity"
                }
            ]
        },

        "career_strategy": {
            "strongest_skill": "Python",
            "strategy_direction": (
                "Focus on Python roles."
            )
        }
    }


def test_generate_readiness_advice():
    result = generate_readiness_advice(
        sample_context()["readiness"]
    )

    assert "47.87%" in result
    assert "foundational skills" in result


def test_generate_strength_advice():
    context = sample_context()

    result = generate_strength_advice(
        context["strengths"],
        context["market_strengths"]
    )

    assert len(result) == 2
    assert "Python" in result[0]
    assert "Python" in result[1]


def test_generate_gap_advice():
    result = generate_gap_advice(
        sample_context()["critical_gaps"]
    )

    assert len(result) == 2
    assert "Git" in result[0]
    assert "REST APIs" in result[1]


def test_generate_market_advice():
    result = generate_market_advice(
        sample_context()["readiness"]
    )

    assert "36.36%" in result
    assert "skill coverage" in result


def test_generate_job_search_advice():
    context = sample_context()

    result = generate_job_search_advice(
        context["top_job_matches"],
        context[
            "readiness_explanation"
        ]["realistic_opportunities"]
    )

    assert len(result) == 2
    assert "Cognizant" in result[0]
    assert "semantic opportunities" in result[1]


def test_generate_learning_plan():
    result = generate_learning_plan(
        sample_context()["critical_gaps"]
    )

    assert len(result) == 2
    assert result[0]["rank"] == 1
    assert result[0]["skill"] == "Git"
    assert result[1]["skill"] == "REST APIs"


def test_generate_application_strategy():
    context = sample_context()

    result = generate_application_strategy(
        context["career_strategy"]
    )

    assert len(result) == 2
    assert "Python" in result[0]
    assert "Focus on Python roles." in result[1]


def test_build_career_advice():
    result = build_career_advice(
        sample_context()
    )

    assert result is not None

    assert "readiness_advice" in result
    assert "strength_advice" in result
    assert "gap_advice" in result
    assert "market_advice" in result
    assert "job_search_advice" in result
    assert "learning_plan" in result
    assert "application_strategy" in result

    assert (
        "47.87%"
        in result["readiness_advice"]
    )

    assert (
        result["learning_plan"][0]["skill"]
        == "Git"
    )


def test_build_career_advice_handles_none():
    result = build_career_advice(
        None
    )

    assert result is None
