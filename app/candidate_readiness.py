PROFICIENCY_SCORES = {
    "Beginner": 60.0,
    "Intermediate": 80.0,
    "Advanced": 100.0
}


def get_readiness_level(readiness_score):
    if readiness_score >= 75:
        return "Job Ready"

    if readiness_score >= 60:
        return "Nearly Job Ready"

    if readiness_score >= 40:
        return "Developing"

    return "Foundation Stage"


def calculate_skill_strength(candidate_skills):
    if not candidate_skills:
        return 0.0

    scores = []

    for skill in candidate_skills:
        proficiency = skill.get(
            "proficiency",
            ""
        )

        score = PROFICIENCY_SCORES.get(
            proficiency,
            0.0
        )

        scores.append(score)

    if not scores:
        return 0.0

    return round(
        sum(scores) / len(scores),
        2
    )


def extract_strongest_skills(candidate_skills):
    ranked_skills = []

    for skill in candidate_skills:
        proficiency = skill.get(
            "proficiency",
            ""
        )

        score = PROFICIENCY_SCORES.get(
            proficiency,
            0.0
        )

        ranked_skills.append({
            "skill": skill["skill"],
            "proficiency": proficiency,
            "strength_score": score
        })

    ranked_skills.sort(
        key=lambda item: item["strength_score"],
        reverse=True
    )

    return ranked_skills


def get_market_coverage(market_item):
    return float(
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
    )


def get_market_job_count(market_item):
    return int(
        market_item.get(
            "job_count",
            market_item.get(
                "jobs",
                market_item.get(
                    "opportunity_count",
                    0
                )
            )
        )
    )


def extract_market_relevant_skills(
    candidate_skills,
    market_skill_demand
):
    market_map = {
        item["skill"].lower(): item
        for item in market_skill_demand
    }

    relevant_skills = []

    for skill in candidate_skills:
        skill_name = skill["skill"]

        market_item = market_map.get(
            skill_name.lower()
        )

        if market_item:
            relevant_skills.append({
                "skill": skill_name,
                "proficiency": skill.get(
                    "proficiency",
                    ""
                ),
                "market_coverage": (
                    get_market_coverage(
                        market_item
                    )
                ),
                "jobs": get_market_job_count(
                    market_item
                )
            })

    relevant_skills.sort(
        key=lambda item: (
            item["market_coverage"],
            item["jobs"]
        ),
        reverse=True
    )

    return relevant_skills


def extract_major_blockers(
    skill_priorities
):
    blockers = []

    for priority in skill_priorities:
        if (
            priority.get(
                "candidate_proficiency"
            ) == "Missing"
        ):
            blockers.append({
                "skill": priority["skill"],
                "priority": priority.get(
                    "priority_category",
                    "Low Priority"
                ),
                "priority_score": priority.get(
                    "priority_score",
                    0.0
                ),
                "required_count": priority.get(
                    "required_count",
                    0
                ),
                "market_coverage": priority.get(
                    "market_coverage",
                    0.0
                )
            })

    blockers.sort(
        key=lambda item: item["priority_score"],
        reverse=True
    )

    return blockers


def calculate_job_fit_score(job_matches):
    if not job_matches:
        return 0.0

    top_matches = sorted(
        job_matches,
        key=lambda item: item.get(
            "combined_match",
            0.0
        ),
        reverse=True
    )[:5]

    scores = [
        item.get(
            "combined_match",
            0.0
        )
        for item in top_matches
    ]

    if not scores:
        return 0.0

    return round(
        sum(scores) / len(scores),
        2
    )


def calculate_market_alignment(
    candidate_skills,
    market_skill_demand
):
    if not candidate_skills:
        return 0.0

    if not market_skill_demand:
        return 0.0

    market_map = {
        item["skill"].lower(): item
        for item in market_skill_demand
    }

    matched_demand = []

    for skill in candidate_skills:
        market_item = market_map.get(
            skill["skill"].lower()
        )

        if market_item:
            demand = get_market_coverage(
                market_item
            )

            matched_demand.append(
                demand
            )

    if not matched_demand:
        return 0.0

    return round(
        min(
            sum(matched_demand),
            100.0
        ),
        2
    )


def count_semantic_opportunities(
    job_matches
):
    return sum(
        1
        for job in job_matches
        if job.get("opportunity_type")
        == "Semantic Opportunity"
    )


def calculate_readiness_score(
    skill_strength,
    job_fit,
    market_alignment
):
    score = (
        skill_strength * 0.40
        + job_fit * 0.40
        + market_alignment * 0.20
    )

    return round(
        min(score, 100.0),
        2
    )


def build_candidate_readiness_profile(
    candidate_skills,
    job_matches,
    skill_priorities,
    market_skill_demand
):
    skill_strength = calculate_skill_strength(
        candidate_skills
    )

    strongest_skills = extract_strongest_skills(
        candidate_skills
    )

    market_relevant_skills = (
        extract_market_relevant_skills(
            candidate_skills,
            market_skill_demand
        )
    )

    major_blockers = extract_major_blockers(
        skill_priorities
    )

    job_fit = calculate_job_fit_score(
        job_matches
    )

    market_alignment = calculate_market_alignment(
        candidate_skills,
        market_skill_demand
    )

    semantic_opportunities = (
        count_semantic_opportunities(
            job_matches
        )
    )

    readiness_score = calculate_readiness_score(
        skill_strength,
        job_fit,
        market_alignment
    )

    return {
        "readiness_score": readiness_score,
        "readiness_level": get_readiness_level(
            readiness_score
        ),
        "skill_strength": skill_strength,
        "job_fit": job_fit,
        "market_alignment": market_alignment,
        "strongest_skills": strongest_skills,
        "market_relevant_skills": (
            market_relevant_skills
        ),
        "major_blockers": major_blockers,
        "semantic_opportunity_count": (
            semantic_opportunities
        )
    }
