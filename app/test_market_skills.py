from database_jobs import get_all_jobs

from job_skill_manager import get_all_job_skills

from market_skill_analyzer import (
    analyze_skill_demand
)


jobs = get_all_jobs()

job_skills_map = get_all_job_skills()


skill_demand = analyze_skill_demand(
    jobs,
    job_skills_map
)


print("Job Market Skill Demand")
print("=======================")


for rank, demand in enumerate(
    skill_demand,
    start=1
):

    print()

    print(
        f"{rank}. {demand['skill']}"
    )

    print(
        "Jobs:",
        demand["job_count"]
    )

    print(
        "Required:",
        demand["required_count"]
    )

    print(
        "Preferred:",
        demand["preferred_count"]
    )

    print(
        "Demand:",
        demand["demand_percentage"],
        "%"
    )
