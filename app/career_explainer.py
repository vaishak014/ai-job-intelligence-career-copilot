def explain_skill_priority(priority, total_jobs):
    skill = priority["skill"]
    proficiency = priority.get("candidate_proficiency", "Missing")
    market_coverage = priority.get("market_coverage", 0.0)
    opportunity_count = priority.get("opportunity_count", 0)
    required_count = priority.get("required_count", 0)
    preferred_count = priority.get("preferred_count", 0)
    priority_category = priority.get(
        "priority_category",
        "Low Priority"
    )
    priority_score = priority.get(
        "priority_score",
        0.0
    )

    if proficiency == "Missing":
        proficiency_text = (
            "You currently have no listed "
            f"proficiency in {skill}."
        )
    else:
        proficiency_text = (
            f"Your current proficiency is "
            f"{proficiency}."
        )

    if total_jobs > 0:
        market_text = (
            f"{skill} appears in "
            f"{opportunity_count} of {total_jobs} "
            "target-role jobs "
            f"({market_coverage}%)."
        )
    else:
        market_text = (
            f"No target-role market data is "
            f"available for {skill}."
        )

    if required_count > 0:
        requirement_text = (
            f"It is required in "
            f"{required_count} of those "
            "opportunities."
        )
    elif preferred_count > 0:
        requirement_text = (
            f"It appears as a preferred skill "
            f"in {preferred_count} opportunities."
        )
    else:
        requirement_text = (
            "No requirement-level information "
            "is available."
        )

    if proficiency == "Missing":
        action_text = (
            f"Learning {skill} would directly "
            "increase your eligibility for "
            "these opportunities."
        )
    elif proficiency == "Beginner":
        action_text = (
            f"Improving your {skill} proficiency "
            "could increase your competitiveness."
        )
    elif proficiency == "Intermediate":
        action_text = (
            f"Strengthening your {skill} proficiency "
            "could improve your competitiveness."
        )
    else:
        action_text = (
            f"{skill} is already an established "
            "skill in your profile."
        )

    return {
        "skill": skill,
        "priority_category": priority_category,
        "priority_score": priority_score,
        "candidate_proficiency": proficiency,
        "market_coverage": market_coverage,
        "opportunity_count": opportunity_count,
        "required_count": required_count,
        "preferred_count": preferred_count,
        "explanation": [
            market_text,
            proficiency_text,
            requirement_text,
            action_text
        ]
    }


def explain_skill_priorities(skill_priorities, total_jobs):
    explanations = []

    for priority in skill_priorities:
        explanations.append(
            explain_skill_priority(
                priority,
                total_jobs
            )
        )

    return explanations


def explain_job_match(job_match):
    explanation = []

    matched_required = job_match.get(
        "matched_required",
        []
    )
    missing_required = job_match.get(
        "missing_required",
        []
    )
    matched_preferred = job_match.get(
        "matched_preferred",
        []
    )
    missing_preferred = job_match.get(
        "missing_preferred",
        []
    )

    for skill in matched_required:
        explanation.append(
            f"✓ {skill} - Required skill matched"
        )

    for skill in missing_required:
        explanation.append(
            f"✗ {skill} - Required skill missing"
        )

    for skill in matched_preferred:
        explanation.append(
            f"✓ {skill} - Preferred skill matched"
        )

    for skill in missing_preferred:
        explanation.append(
            f"⚠ {skill} - Preferred skill missing"
        )

    return {
        "job_id": job_match["job_id"],
        "title": job_match["title"],
        "company": job_match["company"],
        "overall_match": job_match["overall_match"],
        "skill_match_score": job_match.get(
            "skill_match_score",
            job_match["overall_match"]
        ),
        "semantic_similarity": job_match.get(
            "semantic_similarity",
            0.0
        ),
        "combined_match": job_match.get(
            "combined_match",
            job_match["overall_match"]
        ),
        "semantic_signal": job_match.get(
            "semantic_signal",
            "Balanced"
        ),
        "opportunity_type": job_match.get(
            "opportunity_type",
            "Low Relevance"
        ),
        "match_category": job_match["match_category"],
        "explanation": explanation,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred
    }


def explain_job_matches(job_matches):
    explanations = []

    for job_match in job_matches:
        explanations.append(
            explain_job_match(job_match)
        )

    return explanations
