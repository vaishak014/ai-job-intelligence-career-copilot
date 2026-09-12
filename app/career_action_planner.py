def get_action_type(proficiency):
    if proficiency == "Missing":
        return "Learn"
    if proficiency == "Beginner":
        return "Improve"
    if proficiency == "Intermediate":
        return "Strengthen"
    return "Maintain"


def build_action_text(skill, proficiency):
    action_type = get_action_type(proficiency)

    if action_type == "Learn":
        return f"Learn {skill} to increase job eligibility."

    if action_type == "Improve":
        return f"Improve your {skill} proficiency to become more competitive."

    if action_type == "Strengthen":
        return f"Strengthen your {skill} proficiency for stronger job matches."

    return f"Maintain your existing {skill} proficiency."


def create_career_action(priority):
    skill = priority["skill"]
    proficiency = priority.get(
        "candidate_proficiency",
        "Missing"
    )

    return {
        "skill": skill,
        "priority_category": priority.get(
            "priority_category",
            "Low Priority"
        ),
        "priority_score": priority.get(
            "priority_score",
            0.0
        ),
        "candidate_proficiency": proficiency,
        "market_coverage": priority.get(
            "market_coverage",
            0.0
        ),
        "opportunity_count": priority.get(
            "opportunity_count",
            0
        ),
        "required_count": priority.get(
            "required_count",
            0
        ),
        "preferred_count": priority.get(
            "preferred_count",
            0
        ),
        "action_type": get_action_type(proficiency),
        "action": build_action_text(
            skill,
            proficiency
        ),
        "job_ids": priority.get(
            "job_ids",
            []
        ),
        "job_titles": priority.get(
            "job_titles",
            []
        )
    }


def build_career_action_plan(skill_priorities):
    actions = []

    for priority in skill_priorities:
        actions.append(
            create_career_action(priority)
        )

    actions.sort(
        key=lambda item: item["priority_score"],
        reverse=True
    )

    return actions
