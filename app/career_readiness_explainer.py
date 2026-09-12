def build_readiness_summary(
    candidate_readiness,
    candidate_segmentation
):
    readiness_score = candidate_readiness.get(
        "readiness_score",
        0.0
    )

    readiness_level = candidate_readiness.get(
        "readiness_level",
        "Unknown"
    )

    profile_type = candidate_segmentation.get(
        "profile_type",
        "Unknown"
    )

    if readiness_level == "Job Ready":
        summary = (
            "The candidate is currently in a strong "
            "position to pursue target-role opportunities."
        )

    elif readiness_level == "Nearly Job Ready":
        summary = (
            "The candidate has a solid foundation and "
            "needs targeted improvement in a few areas "
            "to become strongly job-ready."
        )

    elif readiness_level == "Developing":
        summary = (
            "The candidate has relevant foundational "
            "skills, but current job fit and skill gaps "
            "limit competitiveness across the market."
        )

    else:
        summary = (
            "The candidate is still developing the core "
            "skills and market alignment needed for "
            "target-role opportunities."
        )

    return {
        "readiness_score": readiness_score,
        "readiness_level": readiness_level,
        "candidate_segment": profile_type,
        "summary": summary
    }


def identify_what_is_helping(
    candidate_readiness,
    candidate_strength_gap
):
    helping = []

    strongest_skills = candidate_readiness.get(
        "strongest_skills",
        []
    )

    market_strengths = candidate_readiness.get(
        "market_relevant_skills",
        []
    )

    semantic_opportunities = candidate_readiness.get(
        "semantic_opportunity_count",
        0
    )

    if strongest_skills:
        top_skills = [
            skill["skill"]
            for skill in strongest_skills[:3]
        ]

        helping.append({
            "factor": "Core Skills",
            "details": (
                "The candidate has established "
                "competence in: "
                + ", ".join(top_skills)
                + "."
            )
        })

    if market_strengths:
        top_market_skills = [
            skill["skill"]
            for skill in market_strengths[:3]
        ]

        helping.append({
            "factor": "Market-Relevant Skills",
            "details": (
                "Existing skills with measurable market "
                "demand include: "
                + ", ".join(top_market_skills)
                + "."
            )
        })

    if semantic_opportunities > 0:
        helping.append({
            "factor": "Semantic Opportunities",
            "details": (
                f"{semantic_opportunities} target-role "
                "opportunities show meaningful semantic "
                "relevance beyond direct skill matching."
            )
        })

    competitive_advantages = candidate_strength_gap.get(
        "competitive_advantages",
        []
    )

    if competitive_advantages:
        advantage_skills = [
            item["skill"]
            for item in competitive_advantages[:3]
        ]

        helping.append({
            "factor": "Competitive Advantages",
            "details": (
                "Advanced skills with market demand "
                "provide additional differentiation: "
                + ", ".join(advantage_skills)
                + "."
            )
        })

    if not helping:
        helping.append({
            "factor": "Current Foundation",
            "details": (
                "The candidate has a starting foundation "
                "that can be developed through targeted "
                "skill improvement."
            )
        })

    return helping


def identify_what_is_holding_back(
    candidate_readiness,
    candidate_strength_gap,
    job_matches
):
    blockers = []

    job_fit = candidate_readiness.get(
        "job_fit",
        0.0
    )

    market_alignment = candidate_readiness.get(
        "market_alignment",
        0.0
    )

    critical_gaps = candidate_strength_gap.get(
        "critical_gaps",
        []
    )

    if job_fit < 40:
        blockers.append({
            "factor": "Job Fit",
            "details": (
                f"Current average top-job fit is only "
                f"{job_fit}%, indicating limited direct "
                "alignment with many target opportunities."
            )
        })

    if market_alignment < 40:
        blockers.append({
            "factor": "Market Alignment",
            "details": (
                f"Current market alignment is "
                f"{market_alignment}%, so the existing "
                "skill set does not yet cover enough of "
                "the skills demanded by the target market."
            )
        })

    for gap in critical_gaps[:3]:
        blockers.append({
            "factor": "Critical Skill Gap",
            "skill": gap["skill"],
            "details": (
                f"{gap['skill']} is currently missing "
                f"and is required in "
                f"{gap['required_count']} target jobs."
            )
        })

    if not job_matches:
        blockers.append({
            "factor": "Opportunity Coverage",
            "details": (
                "There are currently no target-role "
                "job matches available for evaluation."
            )
        })

    return blockers


def build_priority_actions(
    candidate_strength_gap
):
    critical_gaps = candidate_strength_gap.get(
        "critical_gaps",
        []
    )

    actions = []

    for rank, gap in enumerate(
        critical_gaps[:3],
        start=1
    ):
        actions.append({
            "rank": rank,
            "skill": gap["skill"],
            "priority": gap.get(
                "priority_category",
                "Low Priority"
            ),
            "priority_score": gap.get(
                "priority_score",
                0.0
            ),
            "action": (
                f"Develop practical proficiency in "
                f"{gap['skill']} because it is a "
                "high-impact gap in the current "
                "target-role market."
            )
        })

    if not actions:
        actions.append({
            "rank": 1,
            "skill": None,
            "priority": "Maintain",
            "priority_score": 0.0,
            "action": (
                "Maintain current skills while "
                "continuing to build practical "
                "project experience."
            )
        })

    return actions


def identify_realistic_opportunities(
    job_matches
):
    opportunities = []

    for job in job_matches:
        opportunity_type = job.get(
            "opportunity_type",
            "Low Relevance"
        )

        combined_match = job.get(
            "combined_match",
            0.0
        )

        if (
            opportunity_type in [
                "Strong Match",
                "Semantic Opportunity",
                "Skill Match"
            ]
            or combined_match >= 30
        ):
            opportunities.append({
                "job_id": job["job_id"],
                "title": job["title"],
                "company": job["company"],
                "combined_match": combined_match,
                "skill_match_score": job.get(
                    "skill_match_score",
                    0.0
                ),
                "semantic_similarity": job.get(
                    "semantic_similarity",
                    0.0
                ),
                "opportunity_type": opportunity_type
            })

    opportunities.sort(
        key=lambda item: item["combined_match"],
        reverse=True
    )

    return opportunities[:5]


def generate_career_direction(
    candidate_readiness,
    candidate_strength_gap,
    candidate_segmentation
):
    readiness_level = candidate_readiness.get(
        "readiness_level",
        "Unknown"
    )

    profile_type = candidate_segmentation.get(
        "profile_type",
        "Unknown"
    )

    critical_gaps = candidate_strength_gap.get(
        "critical_gaps",
        []
    )

    if readiness_level == "Job Ready":
        return (
            "Focus on applying to suitable target roles, "
            "interview preparation, and converting strong "
            "skill alignment into applications."
        )

    if profile_type == "Semantic-Potential Candidate":
        return (
            "Use semantically relevant opportunities as "
            "learning and application targets while "
            "closing the most important direct skill gaps."
        )

    if critical_gaps:
        return (
            "Prioritize the highest-impact missing skills "
            "before broadening the job search. Build "
            "practical projects around those skills."
        )

    return (
        "Continue strengthening the existing foundation "
        "through practical projects and targeted "
        "market-relevant skill development."
    )


def build_career_readiness_explanation(
    candidate_readiness,
    candidate_segmentation,
    candidate_strength_gap,
    job_matches
):
    summary = build_readiness_summary(
        candidate_readiness,
        candidate_segmentation
    )

    what_is_helping = identify_what_is_helping(
        candidate_readiness,
        candidate_strength_gap
    )

    what_is_holding_back = (
        identify_what_is_holding_back(
            candidate_readiness,
            candidate_strength_gap,
            job_matches
        )
    )

    priority_actions = build_priority_actions(
        candidate_strength_gap
    )

    realistic_opportunities = (
        identify_realistic_opportunities(
            job_matches
        )
    )

    career_direction = generate_career_direction(
        candidate_readiness,
        candidate_strength_gap,
        candidate_segmentation
    )

    return {
        "summary": summary,
        "what_is_helping": what_is_helping,
        "what_is_holding_back": what_is_holding_back,
        "priority_actions": priority_actions,
        "realistic_opportunities": (
            realistic_opportunities
        ),
        "career_direction": career_direction
    }
