from app.database_jobs import (
    get_active_jobs_with_source_metadata
)

from app.job_skill_manager import (
    get_all_job_skills
)

from app.market_skill_analyzer import (
    analyze_skill_demand
)


jobs = get_active_jobs_with_source_metadata(
    source="hopin",
    role_type="Software Engineering"
)

job_skills = get_all_job_skills()

results = analyze_skill_demand(
    jobs,
    job_skills
)

print(
    "Software Engineering jobs:",
    len(jobs)
)

print()
print("Skill demand:")

for result in results:
    print(result)
