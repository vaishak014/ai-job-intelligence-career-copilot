def calculate_skill_priority(
    gap,
    total_jobs,
    market_demand=None
):
    if total_jobs == 0:
        return 0.0

    opportunity_count = gap["opportunity_count"]

    if opportunity_count == 0:
        return 0.0

    # If market demand is supplied, use the actual
    # role-specific market coverage.
    if market_demand is not None:
        market_coverage = market_demand / 100
    else:
        market_coverage = (
            opportunity_count / total_jobs
        )

    gap_factor = gap.get(
        "gap_factor",
        1.0
    )

    required_ratio = (
        gap["required_count"]
        / opportunity_count
    )

    importance_multiplier = (
        1 + required_ratio
    )

    priority_score = (
        market_coverage
        * gap_factor
        * importance_multiplier
        * 100
    )

    return round(
        min(priority_score, 100.0),
        2
    )


def get_priority_category(priority_score):
    if priority_score >= 50:
        return "High Priority"

    if priority_score >= 25:
        return "Medium Priority"

    return "Low Priority"


def generate_skill_priorities(
    skill_gaps,
    total_jobs,
    market_skill_demand=None
):
    priorities = []

    market_demand_map = {}

    if market_skill_demand:

        for demand in market_skill_demand:

            market_demand_map[
                demand["skill"].lower()
            ] = demand["demand_percentage"]

    for gap in skill_gaps:

        market_demand = market_demand_map.get(
            gap["skill"].lower()
        )

        priority_score = calculate_skill_priority(
            gap,
            total_jobs,
            market_demand
        )

        market_coverage = (
            market_demand
            if market_demand is not None
            else (
                (
                    gap["opportunity_count"]
                    / total_jobs
                ) * 100
                if total_jobs > 0
                else 0.0
            )
        )

        priorities.append({
            "skill": gap["skill"],
            "candidate_proficiency": gap.get(
                "candidate_proficiency",
                "Missing"
            ),
            "gap_factor": gap.get(
                "gap_factor",
                1.0
            ),
            "required_count": gap["required_count"],
            "preferred_count": gap["preferred_count"],
            "opportunity_count": gap[
                "opportunity_count"
            ],
            "market_coverage": round(
                market_coverage,
                2
            ),
            "priority_score": priority_score,
            "priority_category": (
                get_priority_category(
                    priority_score
                )
            ),
            "job_ids": gap["job_ids"],
            "job_titles": gap["job_titles"]
        })

    priorities.sort(
        key=lambda item: item["priority_score"],
        reverse=True
    )

    return priorities
