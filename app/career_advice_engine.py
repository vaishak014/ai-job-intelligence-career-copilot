def generate_readiness_advice(
    readiness
):
    score = readiness.get(
        "score",
        0.0
    )

    level = readiness.get(
        "level",
        "Unknown"
    )

    if level == "Job Ready":
        return (
            f"Your current readiness score is {score}%. "
            "You are in a strong position to actively "
            "apply for suitable target-role opportunities."
        )

    if level == "Nearly Job Ready":
        return (
            f"Your current readiness score is {score}%. "
            "You have a solid foundation, but targeted "
            "improvements are still needed before you "
            "become strongly competitive."
        )

    if level == "Developing":
        return (
            f"Your current readiness score is {score}%. "
            "You have relevant foundational skills, but "
            "job fit and skill gaps currently limit your "
            "competitiveness."
        )

    return (
        f"Your current readiness score is {score}%. "
        "Focus first on building the core skills required "
        "for your target roles."
    )


def generate_strength_advice(
    strengths,
    market_strengths
):
    advice = []

    if strengths:
        skill_names = [
            item.get("skill", "")
            for item in strengths[:3]
            if item.get("skill")
        ]

        if skill_names:
            advice.append(
                "Your strongest current skills are "
                + ", ".join(skill_names)
                + "."
            )

    if market_strengths:
        market_names = [
            item.get("skill", "")
            for item in market_strengths[:3]
            if item.get("skill")
        ]

        if market_names:
            advice.append(
                "Your most market-relevant existing skills "
                "include "
                + ", ".join(market_names)
                + "."
            )

    if not advice:
        advice.append(
            "Your current skill foundation should be "
            "strengthened through practical projects."
        )

    return advice


def generate_gap_advice(
    critical_gaps
):
    advice = []

    for gap in critical_gaps[:3]:
        skill = gap.get(
            "skill",
            ""
        )

        priority = gap.get(
            "priority_category",
            "Low Priority"
        )

        required_count = gap.get(
            "required_count",
            0
        )

        if not skill:
            continue

        advice.append(
            f"{skill} is a {priority.lower()} gap "
            f"and is required in {required_count} "
            "target-role opportunities."
        )

    if not advice:
        advice.append(
            "No major skill blockers were identified "
            "from the current market data."
        )

    return advice


def generate_market_advice(
    readiness
):
    market_alignment = readiness.get(
        "market_alignment",
        0.0
    )

    if market_alignment >= 60:
        return (
            f"Your market alignment is {market_alignment}%, "
            "indicating that your existing skills have "
            "strong relevance to the target market."
        )

    if market_alignment >= 40:
        return (
            f"Your market alignment is {market_alignment}%. "
            "Your current skills have meaningful market "
            "relevance, but broader coverage would improve "
            "your opportunities."
        )

    return (
        f"Your market alignment is {market_alignment}%. "
        "Expanding your skill coverage with high-demand "
        "skills should improve your access to target roles."
    )


def generate_job_search_advice(
    top_job_matches,
    realistic_opportunities
):
    advice = []

    if top_job_matches:
        best_job = top_job_matches[0]

        title = best_job.get(
            "title",
            "a suitable role"
        )

        company = best_job.get(
            "company",
            ""
        )

        combined_match = best_job.get(
            "combined_match",
            0.0
        )

        if company:
            advice.append(
                f"Your strongest current opportunity is "
                f"{title} at {company}, with a combined "
                f"match of {combined_match}%."
            )
        else:
            advice.append(
                f"Your strongest current opportunity is "
                f"{title}, with a combined match of "
                f"{combined_match}%."
            )

    semantic_count = sum(
        1
        for job in realistic_opportunities
        if job.get("opportunity_type")
        == "Semantic Opportunity"
    )

    if semantic_count > 0:
        advice.append(
            f"{semantic_count} of the currently surfaced "
            "opportunities are semantic opportunities. "
            "These can be useful targets while you close "
            "the associated skill gaps."
        )

    if not advice:
        advice.append(
            "Continue building your skill profile before "
            "expanding your job search."
        )

    return advice


def generate_learning_plan(
    critical_gaps
):
    plan = []

    for rank, gap in enumerate(
        critical_gaps[:3],
        start=1
    ):
        skill = gap.get(
            "skill",
            ""
        )

        if not skill:
            continue

        plan.append({
            "rank": rank,
            "skill": skill,
            "priority": gap.get(
                "priority_category",
                "Low Priority"
            ),
            "reason": (
                f"Develop {skill} because it is "
                "currently one of the highest-impact "
                "missing skills in the target market."
            )
        })

    return plan


def generate_application_strategy(
    career_strategy
):
    strongest_skill = career_strategy.get(
        "strongest_skill"
    )

    strategy_direction = career_strategy.get(
        "strategy_direction",
        ""
    )

    advice = []

    if strongest_skill:
        advice.append(
            f"Use {strongest_skill} as a core skill "
            "when targeting relevant opportunities."
        )

    if strategy_direction:
        advice.append(
            strategy_direction
        )

    if not advice:
        advice.append(
            "Target roles where your strongest existing "
            "skills overlap with current market demand."
        )

    return advice


def build_career_advice(
    copilot_context
):
    if copilot_context is None:
        return None

    readiness = copilot_context.get(
        "readiness",
        {}
    )

    strengths = copilot_context.get(
        "strengths",
        []
    )

    market_strengths = copilot_context.get(
        "market_strengths",
        []
    )

    critical_gaps = copilot_context.get(
        "critical_gaps",
        []
    )

    top_job_matches = copilot_context.get(
        "top_job_matches",
        []
    )

    readiness_explanation = copilot_context.get(
        "readiness_explanation",
        {}
    )

    realistic_opportunities = (
        readiness_explanation.get(
            "realistic_opportunities",
            []
        )
    )

    career_strategy = copilot_context.get(
        "career_strategy",
        {}
    )

    return {
        "readiness_advice": (
            generate_readiness_advice(
                readiness
            )
        ),

        "strength_advice": (
            generate_strength_advice(
                strengths,
                market_strengths
            )
        ),

        "gap_advice": (
            generate_gap_advice(
                critical_gaps
            )
        ),

        "market_advice": (
            generate_market_advice(
                readiness
            )
        ),

        "job_search_advice": (
            generate_job_search_advice(
                top_job_matches,
                realistic_opportunities
            )
        ),

        "learning_plan": (
            generate_learning_plan(
                critical_gaps
            )
        ),

        "application_strategy": (
            generate_application_strategy(
                career_strategy
            )
        )
    }
