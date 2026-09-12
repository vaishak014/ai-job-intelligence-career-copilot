from app.candidate_segmentation import (
    classify_candidate_profile,
    generate_segment_reason,
    build_candidate_segmentation
)


def test_classify_strong_core_candidate():
    result = classify_candidate_profile(
        readiness_score=75.0,
        skill_strength=85.0,
        job_fit=60.0,
        market_alignment=40.0,
        semantic_opportunity_count=0,
        major_blocker_count=2
    )

    assert result == "Strong Core Candidate"


def test_classify_semantic_potential_candidate():
    result = classify_candidate_profile(
        readiness_score=35.0,
        skill_strength=40.0,
        job_fit=30.0,
        market_alignment=20.0,
        semantic_opportunity_count=3,
        major_blocker_count=2
    )

    assert result == "Semantic-Potential Candidate"


def test_classify_market_aligned_candidate():
    result = classify_candidate_profile(
        readiness_score=55.0,
        skill_strength=65.0,
        job_fit=35.0,
        market_alignment=35.0,
        semantic_opportunity_count=0,
        major_blocker_count=2
    )

    assert result == "Market-Aligned Candidate"


def test_classify_skill_gap_heavy_candidate():
    result = classify_candidate_profile(
        readiness_score=30.0,
        skill_strength=40.0,
        job_fit=25.0,
        market_alignment=15.0,
        semantic_opportunity_count=0,
        major_blocker_count=5
    )

    assert result == "Skill-Gap Heavy Candidate"


def test_classify_emerging_candidate():
    result = classify_candidate_profile(
        readiness_score=45.0,
        skill_strength=50.0,
        job_fit=35.0,
        market_alignment=20.0,
        semantic_opportunity_count=0,
        major_blocker_count=2
    )

    assert result == "Emerging Candidate"


def test_classify_foundation_candidate():
    result = classify_candidate_profile(
        readiness_score=20.0,
        skill_strength=20.0,
        job_fit=10.0,
        market_alignment=5.0,
        semantic_opportunity_count=0,
        major_blocker_count=1
    )

    assert result == "Foundation Candidate"


def test_generate_segment_reason():
    result = generate_segment_reason(
        "Strong Core Candidate",
        80.0,
        85.0,
        60.0,
        40.0,
        0,
        1
    )

    assert "strong core skills" in result
    assert "job fit" in result


def test_build_candidate_segmentation():
    candidate_readiness = {
        "readiness_score": 35.0,
        "readiness_level": "Developing",
        "skill_strength": 40.0,
        "job_fit": 30.0,
        "market_alignment": 20.0,
        "semantic_opportunity_count": 3,
        "major_blockers": [
            {
                "skill": "AWS"
            },
            {
                "skill": "Git"
            }
        ]
    }

    result = build_candidate_segmentation(
        candidate_readiness
    )

    assert result["profile_type"] == (
        "Semantic-Potential Candidate"
    )

    assert result["readiness_score"] == 35.0
    assert result["readiness_level"] == "Developing"
    assert result["skill_strength"] == 40.0
    assert result["job_fit"] == 30.0
    assert result["market_alignment"] == 20.0
    assert result["semantic_opportunity_count"] == 3
    assert result["major_blocker_count"] == 2
    assert result["reason"]


def test_build_segmentation_preserves_zero_values():
    candidate_readiness = {
        "readiness_score": 0.0,
        "readiness_level": "Foundation Stage",
        "skill_strength": 0.0,
        "job_fit": 0.0,
        "market_alignment": 0.0,
        "semantic_opportunity_count": 0,
        "major_blockers": []
    }

    result = build_candidate_segmentation(
        candidate_readiness
    )

    assert result["profile_type"] == (
        "Foundation Candidate"
    )

    assert result["readiness_score"] == 0.0
    assert result["skill_strength"] == 0.0
    assert result["job_fit"] == 0.0
    assert result["market_alignment"] == 0.0
    assert result["semantic_opportunity_count"] == 0
    assert result["major_blocker_count"] == 0
