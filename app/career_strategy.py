def get_proficiency_rank(proficiency):
    return {
        "Advanced": 3,
        "Intermediate": 2,
        "Beginner": 1
    }.get(proficiency, 0)


def identify_strongest_skill(
    candidate_skills,
    market_skill_demand=None
):
    if not candidate_skills:
        return None

    market_demand_map = {}

    if market_skill_demand:
        for demand in market_skill_demand:
            market_demand_map[
                demand["skill"].lower()
            ] = demand.get(
                "demand_percentage",
                0.0
            )

    ranked_skills = sorted(
        candidate_skills,
        key=lambda skill: (
            get_proficiency_rank(
                skill.get("proficiency")
            ),
            market_demand_map.get(
                skill["skill"].lower(),
                0.0
            )
        ),
        reverse=True
    )

    return ranked_skills[0]["skill"]


def identify_best_job_match(job_matches):
    if not job_matches:
        return None

    return max(
        job_matches,
        key=lambda job: job.get(
            "overall_match",
            0.0
        )
    )


def identify_top_improvements(
    career_action_plan,
    limit=3
):
    return career_action_plan[:limit]


def determine_strategy_direction(
    candidate_skills,
    job_matches,
    career_action_plan,
    market_skill_demand=None
):
    strongest_skill = identify_strongest_skill(
        candidate_skills,
        market_skill_demand
    )

    best_match = identify_best_job_match(
        job_matches
    )

    if strongest_skill is None:
        return (
            "Build foundational skills before "
            "targeting specific roles."
        )

    if best_match is None:
        return (
            f"Build on your existing {strongest_skill} "
            "skill while developing high-priority "
            "market skills."
        )

    return (
        f"Prioritize opportunities where "
        f"{strongest_skill} is relevant, while "
        "developing the highest-impact skill gaps."
    )


def build_career_strategy(
    candidate_skills,
    job_matches,
    career_action_plan,
    market_skill_demand=None
):
    strongest_skill = identify_strongest_skill(
        candidate_skills,
        market_skill_demand
    )

    best_match = identify_best_job_match(
        job_matches
    )

    top_improvements = identify_top_improvements(
        career_action_plan
    )

    strategy_direction = determine_strategy_direction(
        candidate_skills,
        job_matches,
        career_action_plan,
        market_skill_demand
    )

    return {
        "strongest_skill": strongest_skill,
        "best_job_match": best_match,
        "top_improvements": top_improvements,
        "strategy_direction": strategy_direction
    }
