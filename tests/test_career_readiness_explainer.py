from app.career_readiness_explainer import (
    build_readiness_summary,
    identify_what_is_helping,
    identify_what_is_holding_back,
    build_priority_actions,
    identify_realistic_opportunities,
    generate_career_direction,
    build_career_readiness_explanation
)


def sample_readiness():
    return {
        "readiness_score": 47.87,
        "readiness_level": "Developing",
        "skill_strength": 75.0,
        "job_fit": 26.5,
        "market_alignment": 36.36,
        "semantic_opportunity_count": 4,
        "strongest_skills": [
            {
                "skill": "Python",
                "proficiency": "Intermediate",
                "strength_score": 80.0
            }
        ],
        "market_relevant_skills": [
            {
                "skill": "Python",
                "proficiency": "Intermediate",
                "market_coverage": 18.18,
                "jobs": 2
            }
        ]
    }


def sample_segmentation():
    return {
        "profile_type": "Semantic-Potential Candidate"
    }


def sample_strength_gap():
    return {
        "critical_gaps": [
            {
                "skill": "Git",
                "priority_category": "High Priority",
                "priority_score": 54.54,
                "required_count": 3,
                "market_coverage": 27.27
            },
            {
                "skill": "REST APIs",
                "priority_category": "High Priority",
                "priority_score": 54.54,
                "required_count": 3,
                "market_coverage": 27.27
            }
        ],
        "competitive_advantages": []
    }


def sample_jobs():
    return [
        {
            "job_id": 1,
            "title": "Python Developer",
            "company": "Example",
            "skill_match_score": 53.33,
            "semantic_similarity": 63.42,
            "combined_match": 56.36,
            "opportunity_type": "Strong Match"
        },
        {
            "job_id": 2,
            "title": "Software Engineer",
            "company": "Example Two",
            "skill_match_score": 26.67,
            "semantic_similarity": 56.65,
            "combined_match": 35.66,
            "opportunity_type": "Semantic Opportunity"
        },
        {
            "job_id": 3,
            "title": "Unrelated Role",
            "company": "Example Three",
            "skill_match_score": 5.0,
            "semantic_similarity": 10.0,
            "combined_match": 6.5,
            "opportunity_type": "Low Relevance"
        }
    ]


def test_build_readiness_summary():
    result = build_readiness_summary(
        sample_readiness(),
        sample_segmentation()
    )

    assert result["readiness_score"] == 47.87
    assert result["readiness_level"] == "Developing"
    assert (
        result["candidate_segment"]
        == "Semantic-Potential Candidate"
    )
    assert "foundation" in result["summary"].lower()


def test_identify_what_is_helping():
    result = identify_what_is_helping(
        sample_readiness(),
        sample_strength_gap()
    )

    assert len(result) >= 2
    assert any(
        item["factor"] == "Core Skills"
        for item in result
    )
    assert any(
        item["factor"] == "Market-Relevant Skills"
        for item in result
    )
    assert any(
        item["factor"] == "Semantic Opportunities"
        for item in result
    )


def test_identify_what_is_holding_back():
    result = identify_what_is_holding_back(
        sample_readiness(),
        sample_strength_gap(),
        sample_jobs()
    )

    assert any(
        item["factor"] == "Job Fit"
        for item in result
    )

    assert any(
        item["factor"] == "Market Alignment"
        for item in result
    )

    assert any(
        item.get("skill") == "Git"
        for item in result
    )


def test_build_priority_actions():
    result = build_priority_actions(
        sample_strength_gap()
    )

    assert len(result) == 2
    assert result[0]["rank"] == 1
    assert result[0]["skill"] == "Git"
    assert result[0]["priority"] == "High Priority"


def test_identify_realistic_opportunities():
    result = identify_realistic_opportunities(
        sample_jobs()
    )

    assert len(result) == 2
    assert result[0]["title"] == "Python Developer"
    assert (
        result[1]["opportunity_type"]
        == "Semantic Opportunity"
    )


def test_generate_career_direction():
    result = generate_career_direction(
        sample_readiness(),
        sample_strength_gap(),
        sample_segmentation()
    )

    assert "semantic" in result.lower()
    assert "skill" in result.lower()


def test_build_career_readiness_explanation():
    result = build_career_readiness_explanation(
        sample_readiness(),
        sample_segmentation(),
        sample_strength_gap(),
        sample_jobs()
    )

    assert "summary" in result
    assert "what_is_helping" in result
    assert "what_is_holding_back" in result
    assert "priority_actions" in result
    assert "realistic_opportunities" in result
    assert "career_direction" in result

    assert result["summary"]["readiness_score"] == 47.87
    assert len(result["priority_actions"]) == 2
    assert len(result["realistic_opportunities"]) == 2
