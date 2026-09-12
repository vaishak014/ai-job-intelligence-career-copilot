def analyze_skill_demand(
    jobs,
    job_skills_map
):
    """
    Analyze skill demand across the supplied jobs.

    Demand percentage uses the total number of supplied
    jobs as the denominator.

    Each job contributes at most once per skill.
    """

    total_jobs = len(jobs)

    if total_jobs == 0:
        return []

    skill_demand = {}

    for job in jobs:

        job_id = job["job_id"]

        job_skills = job_skills_map.get(
            job_id,
            []
        )

        skills_seen_for_job = set()

        for job_skill in job_skills:

            skill_name = job_skill["skill"]

            if skill_name in skills_seen_for_job:
                continue

            skills_seen_for_job.add(
                skill_name
            )

            if skill_name not in skill_demand:

                skill_demand[skill_name] = {
                    "skill": skill_name,
                    "job_count": 0,
                    "required_count": 0,
                    "preferred_count": 0
                }

            skill_demand[
                skill_name
            ]["job_count"] += 1

            importance = job_skill["importance"]

            if importance == "Required":
                skill_demand[
                    skill_name
                ]["required_count"] += 1

            elif importance == "Preferred":
                skill_demand[
                    skill_name
                ]["preferred_count"] += 1

    for demand in skill_demand.values():

        demand["demand_percentage"] = round(
            (
                demand["job_count"]
                / total_jobs
            ) * 100,
            2
        )

        demand["required_percentage"] = round(
            (
                demand["required_count"]
                / total_jobs
            ) * 100,
            2
        )

        demand["preferred_percentage"] = round(
            (
                demand["preferred_count"]
                / total_jobs
            ) * 100,
            2
        )

    ranked_demand = sorted(
        skill_demand.values(),
        key=lambda item: (
            item["job_count"],
            item["required_count"],
            item["preferred_count"]
        ),
        reverse=True
    )

    return ranked_demand
