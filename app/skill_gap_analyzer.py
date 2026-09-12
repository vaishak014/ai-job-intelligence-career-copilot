def get_candidate_skill_proficiencies(candidate_skills):
    return {
        skill["skill"].lower(): skill["proficiency"]
        for skill in candidate_skills
    }


def get_proficiency_gap_factor(proficiency):
    """
    Convert candidate proficiency into a learning-gap factor.

    Higher value means a larger opportunity for improvement.
    """
    factors = {
        "Advanced": 0.0,
        "Intermediate": 0.4,
        "Beginner": 0.75
    }

    if proficiency is None:
        return 1.0

    return factors.get(
        str(proficiency).strip().title(),
        1.0
    )


def analyze_skill_gaps(
    candidate_skills,
    jobs,
    job_skills_map
):
    candidate_proficiencies = (
        get_candidate_skill_proficiencies(
            candidate_skills
        )
    )

    skill_gaps = {}

    for job in jobs:

        job_id = job["job_id"]

        job_skills = job_skills_map.get(
            job_id,
            []
        )

        skills_seen_for_job = set()

        for job_skill in job_skills:

            skill_name = job_skill["skill"]
            skill_key = skill_name.lower()
            importance = job_skill["importance"]

            if skill_key in skills_seen_for_job:
                continue

            skills_seen_for_job.add(skill_key)

            proficiency = candidate_proficiencies.get(
                skill_key
            )

            gap_factor = get_proficiency_gap_factor(
                proficiency
            )

            # Advanced candidates do not have a learning gap
            # for that skill.
            if gap_factor == 0.0:
                continue

            if skill_name not in skill_gaps:

                skill_gaps[skill_name] = {
                    "skill": skill_name,
                    "candidate_proficiency": (
                        proficiency
                        if proficiency is not None
                        else "Missing"
                    ),
                    "gap_factor": gap_factor,
                    "required_count": 0,
                    "preferred_count": 0,
                    "job_ids": [],
                    "job_titles": []
                }

            if importance == "Required":
                skill_gaps[
                    skill_name
                ]["required_count"] += 1

            else:
                skill_gaps[
                    skill_name
                ]["preferred_count"] += 1

            if job_id not in skill_gaps[
                skill_name
            ]["job_ids"]:

                skill_gaps[
                    skill_name
                ]["job_ids"].append(job_id)

                skill_gaps[
                    skill_name
                ]["job_titles"].append(
                    job["title"]
                )

    for gap in skill_gaps.values():

        gap["opportunity_count"] = (
            gap["required_count"]
            + gap["preferred_count"]
        )

        gap["priority_score"] = (
            gap["required_count"] * 2
            + gap["preferred_count"]
        )

    ranked_gaps = sorted(
        skill_gaps.values(),
        key=lambda gap: (
            gap["priority_score"],
            gap["opportunity_count"]
        ),
        reverse=True
    )

    return ranked_gaps
