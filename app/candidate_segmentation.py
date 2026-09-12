def classify_candidate_profile(
    readiness_score,
    skill_strength,
    job_fit,
    market_alignment,
    semantic_opportunity_count,
    major_blocker_count
):
    if (
        skill_strength >= 75
        and job_fit >= 50
        and major_blocker_count <= 2
    ):
        return "Strong Core Candidate"

    if (
        semantic_opportunity_count >= 2
        and job_fit < 40
    ):
        return "Semantic-Potential Candidate"

    if (
        market_alignment >= 30
        and skill_strength >= 60
    ):
        return "Market-Aligned Candidate"

    if major_blocker_count >= 4:
        return "Skill-Gap Heavy Candidate"

    if readiness_score >= 40:
        return "Emerging Candidate"

    return "Foundation Candidate"


def generate_segment_reason(
    profile_type,
    readiness_score,
    skill_strength,
    job_fit,
    market_alignment,
    semantic_opportunity_count,
    major_blocker_count
):
    if profile_type == "Strong Core Candidate":
        return (
            "The candidate has strong core skills, "
            "reasonable job fit, and relatively few "
            "major skill blockers."
        )

    if profile_type == "Semantic-Potential Candidate":
        return (
            "The candidate has multiple jobs with "
            "meaningful semantic relevance despite "
            "limited direct skill-match scores."
        )

    if profile_type == "Market-Aligned Candidate":
        return (
            "The candidate's existing skills show "
            "meaningful alignment with the skills "
            "currently demanded in the target market."
        )

    if profile_type == "Skill-Gap Heavy Candidate":
        return (
            "Several high-impact skill gaps currently "
            "limit the candidate's eligibility across "
            "target-role opportunities."
        )

    if profile_type == "Emerging Candidate":
        return (
            "The candidate has a developing foundation "
            "with some relevant skills but still needs "
            "targeted improvement to become strongly "
            "competitive."
        )

    return (
        "The candidate is still building the core "
        "skills and market alignment needed for "
        "target-role opportunities."
    )


def build_candidate_segmentation(
    candidate_readiness
):
    readiness_score = candidate_readiness.get(
        "readiness_score",
        0.0
    )

    skill_strength = candidate_readiness.get(
        "skill_strength",
        0.0
    )

    job_fit = candidate_readiness.get(
        "job_fit",
        0.0
    )

    market_alignment = candidate_readiness.get(
        "market_alignment",
        0.0
    )

    semantic_opportunity_count = (
        candidate_readiness.get(
            "semantic_opportunity_count",
            0
        )
    )

    major_blockers = candidate_readiness.get(
        "major_blockers",
        []
    )

    major_blocker_count = len(
        major_blockers
    )

    profile_type = classify_candidate_profile(
        readiness_score,
        skill_strength,
        job_fit,
        market_alignment,
        semantic_opportunity_count,
        major_blocker_count
    )

    reason = generate_segment_reason(
        profile_type,
        readiness_score,
        skill_strength,
        job_fit,
        market_alignment,
        semantic_opportunity_count,
        major_blocker_count
    )

    return {
        "profile_type": profile_type,
        "reason": reason,
        "readiness_score": readiness_score,
        "readiness_level": candidate_readiness.get(
            "readiness_level",
            "Unknown"
        ),
        "skill_strength": skill_strength,
        "job_fit": job_fit,
        "market_alignment": market_alignment,
        "semantic_opportunity_count": (
            semantic_opportunity_count
        ),
        "major_blocker_count": (
            major_blocker_count
        )
    }
