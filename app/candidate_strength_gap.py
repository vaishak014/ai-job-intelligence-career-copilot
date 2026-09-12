def build_candidate_skill_map(candidate_skills):
    return {
        skill["skill"].lower(): skill
        for skill in candidate_skills
    }


def extract_candidate_strengths(candidate_skills):
    strengths = []

    proficiency_scores = {
        "Beginner": 60.0,
        "Intermediate": 80.0,
        "Advanced": 100.0
    }

    for skill in candidate_skills:
        proficiency = skill.get(
            "proficiency",
            ""
        )

        strength_score = proficiency_scores.get(
            proficiency,
            0.0
        )

        strengths.append({
            "skill": skill["skill"],
            "proficiency": proficiency,
            "strength_score": strength_score
        })

    strengths.sort(
        key=lambda item: item["strength_score"],
        reverse=True
    )

    return strengths


def extract_market_strengths(
    candidate_skills,
    market_skill_demand
):
    market_map = {
        item["skill"].lower(): item
        for item in market_skill_demand
    }

    strengths = []

    for skill in candidate_skills:
        skill_name = skill["skill"]

        market_item = market_map.get(
            skill_name.lower()
        )

        if not market_item:
            continue

        demand = market_item.get(
            "demand_percentage",
            market_item.get(
                "demand",
                market_item.get(
                    "market_coverage",
                    0.0
                )
            )
        )

        job_count = market_item.get(
            "job_count",
            market_item.get(
                "jobs",
                market_item.get(
                    "opportunity_count",
                    0
                )
            )
        )

        strengths.append({
            "skill": skill_name,
            "proficiency": skill.get(
                "proficiency",
                ""
            ),
            "market_demand": float(demand),
            "job_count": int(job_count)
        })

    strengths.sort(
        key=lambda item: (
            item["market_demand"],
            item["job_count"]
        ),
        reverse=True
    )

    return strengths


def extract_critical_gaps(
    skill_priorities
):
    gaps = []

    for priority in skill_priorities:
        if (
            priority.get(
                "candidate_proficiency"
            ) != "Missing"
        ):
            continue

        required_count = priority.get(
            "required_count",
            0
        )

        priority_score = priority.get(
            "priority_score",
            0.0
        )

        if required_count > 0:
            gaps.append({
                "skill": priority["skill"],
                "priority_category": priority.get(
                    "priority_category",
                    "Low Priority"
                ),
                "priority_score": priority_score,
                "required_count": required_count,
                "market_coverage": priority.get(
                    "market_coverage",
                    0.0
                )
            })

    gaps.sort(
        key=lambda item: (
            item["priority_score"],
            item["required_count"]
        ),
        reverse=True
    )

    return gaps


def extract_opportunity_gaps(
    job_matches,
    skill_priorities
):
    semantic_jobs = [
        job
        for job in job_matches
        if job.get("opportunity_type")
        == "Semantic Opportunity"
    ]

    if not semantic_jobs:
        return []

    priority_map = {
        priority["skill"].lower(): priority
        for priority in skill_priorities
    }

    gap_map = {}

    for job in semantic_jobs:
        for skill in job.get(
            "missing_required",
            []
        ):
            priority = priority_map.get(
                skill.lower()
            )

            if not priority:
                continue

            skill_name = priority["skill"]

            if skill_name not in gap_map:
                gap_map[skill_name] = {
                    "skill": skill_name,
                    "semantic_jobs": 0,
                    "required_count": priority.get(
                        "required_count",
                        0
                    ),
                    "priority_score": priority.get(
                        "priority_score",
                        0.0
                    ),
                    "market_coverage": priority.get(
                        "market_coverage",
                        0.0
                    )
                }

            gap_map[skill_name][
                "semantic_jobs"
            ] += 1

    gaps = list(
        gap_map.values()
    )

    gaps.sort(
        key=lambda item: (
            item["semantic_jobs"],
            item["priority_score"]
        ),
        reverse=True
    )

    return gaps


def identify_competitive_advantages(
    candidate_skills,
    market_skill_demand
):
    market_map = {
        item["skill"].lower(): item
        for item in market_skill_demand
    }

    advantages = []

    for skill in candidate_skills:
        market_item = market_map.get(
            skill["skill"].lower()
        )

        if not market_item:
            continue

        proficiency = skill.get(
            "proficiency",
            ""
        )

        if proficiency == "Advanced":
            advantages.append({
                "skill": skill["skill"],
                "proficiency": proficiency,
                "market_demand": float(
                    market_item.get(
                        "demand_percentage",
                        market_item.get(
                            "demand",
                            market_item.get(
                                "market_coverage",
                                0.0
                            )
                        )
                    )
                ),
                "reason": (
                    "Advanced proficiency combined "
                    "with measurable market demand."
                )
            })

    advantages.sort(
        key=lambda item: item["market_demand"],
        reverse=True
    )

    return advantages


def build_candidate_strength_gap_analysis(
    candidate_skills,
    job_matches,
    skill_priorities,
    market_skill_demand
):
    strengths = extract_candidate_strengths(
        candidate_skills
    )

    market_strengths = extract_market_strengths(
        candidate_skills,
        market_skill_demand
    )

    critical_gaps = extract_critical_gaps(
        skill_priorities
    )

    opportunity_gaps = extract_opportunity_gaps(
        job_matches,
        skill_priorities
    )

    competitive_advantages = (
        identify_competitive_advantages(
            candidate_skills,
            market_skill_demand
        )
    )

    return {
        "strengths": strengths,
        "market_strengths": market_strengths,
        "critical_gaps": critical_gaps,
        "opportunity_gaps": opportunity_gaps,
        "competitive_advantages": (
            competitive_advantages
        )
    }
