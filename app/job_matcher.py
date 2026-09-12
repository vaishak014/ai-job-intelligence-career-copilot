PROFICIENCY_SCORES = {
    "Beginner": 0.6,
    "Intermediate": 0.8,
    "Advanced": 1.0
}


PREFERRED_BONUS_WEIGHT = 0.20


def calculate_group_score(
    candidate_skill_map,
    job_skills
):
    if not job_skills:
        return 0.0

    total_score = 0.0

    for job_skill in job_skills:

        candidate_skill = candidate_skill_map.get(
            job_skill["skill"].lower()
        )

        if candidate_skill:

            total_score += PROFICIENCY_SCORES.get(
                candidate_skill["proficiency"],
                0.5
            )

    return (
        total_score / len(job_skills)
    ) * 100


def get_match_category(score):
    if score >= 90:
        return "Excellent Match"

    if score >= 75:
        return "Strong Match"

    if score >= 60:
        return "Moderate Match"

    if score >= 40:
        return "Weak Match"

    return "Low Match"


def calculate_skill_match(
    candidate_skills,
    job_skills
):
    candidate_skill_map = {
        item["skill"].lower(): item
        for item in candidate_skills
    }

    required_skills = [
        item
        for item in job_skills
        if item["importance"] == "Required"
    ]

    preferred_skills = [
        item
        for item in job_skills
        if item["importance"] == "Preferred"
    ]

    matched_required = []
    missing_required = []

    matched_preferred = []
    missing_preferred = []

    skill_details = []

    for job_skill in job_skills:

        skill_name = job_skill["skill"]
        importance = job_skill["importance"]

        candidate_skill = candidate_skill_map.get(
            skill_name.lower()
        )

        if candidate_skill:

            proficiency = candidate_skill["proficiency"]

            proficiency_score = PROFICIENCY_SCORES.get(
                proficiency,
                0.5
            )

            if importance == "Required":
                matched_required.append(
                    skill_name
                )
            else:
                matched_preferred.append(
                    skill_name
                )

            skill_details.append({
                "skill": skill_name,
                "importance": importance,
                "status": "Matched",
                "proficiency": proficiency,
                "contribution": round(
                    proficiency_score * 100,
                    2
                )
            })

        else:

            if importance == "Required":
                missing_required.append(
                    skill_name
                )
            else:
                missing_preferred.append(
                    skill_name
                )

            skill_details.append({
                "skill": skill_name,
                "importance": importance,
                "status": "Missing",
                "proficiency": None,
                "contribution": 0
            })

    required_fit = calculate_group_score(
        candidate_skill_map,
        required_skills
    )

    preferred_fit = calculate_group_score(
        candidate_skill_map,
        preferred_skills
    )

    preferred_bonus = (
        preferred_fit * PREFERRED_BONUS_WEIGHT
    )

    if required_skills:

        overall_match = (
            required_fit + preferred_bonus
        )

    elif preferred_skills:

        overall_match = preferred_fit

    else:

        overall_match = 0.0

    overall_match = min(
        round(overall_match, 2),
        100.0
    )

    return {
        "required_fit": round(
            required_fit,
            2
        ),
        "preferred_fit": round(
            preferred_fit,
            2
        ),
        "preferred_bonus": round(
            preferred_bonus,
            2
        ),
        "overall_match": overall_match,
        "match_category": get_match_category(
            overall_match
        ),
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "skill_details": skill_details
    }


def rank_jobs(
    candidate_skills,
    jobs,
    job_skills_map
):
    ranked_jobs = []

    for job in jobs:

        job_skills = job_skills_map.get(
            job["job_id"],
            []
        )

        result = calculate_skill_match(
            candidate_skills,
            job_skills
        )

        ranked_jobs.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company"],
            "required_fit": result[
                "required_fit"
            ],
            "preferred_fit": result[
                "preferred_fit"
            ],
            "preferred_bonus": result[
                "preferred_bonus"
            ],
            "overall_match": result[
                "overall_match"
            ],
            "match_category": result[
                "match_category"
            ],
            "matched_required": result[
                "matched_required"
            ],
            "missing_required": result[
                "missing_required"
            ],
            "matched_preferred": result[
                "matched_preferred"
            ],
            "missing_preferred": result[
                "missing_preferred"
            ],
            "skill_details": result[
                "skill_details"
            ]
        })

    ranked_jobs.sort(
        key=lambda job: job["overall_match"],
        reverse=True
    )

    return ranked_jobs
