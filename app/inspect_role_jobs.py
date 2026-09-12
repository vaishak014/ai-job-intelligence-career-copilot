from app.database_jobs import (
    get_active_jobs_with_source_metadata
)


jobs = get_active_jobs_with_source_metadata(
    source="hopin",
    role_type="Software Engineering"
)

print(
    "Software Engineering jobs:",
    len(jobs)
)

for job in jobs:
    print(
        job["job_id"],
        "|",
        job["title"],
        "|",
        job["source_role_type"]
    )


print()
print("Active Hopin jobs:")

hopin_jobs = get_active_jobs_with_source_metadata(
    source="hopin"
)

print(
    "Count:",
    len(hopin_jobs)
)

if hopin_jobs:
    print(hopin_jobs[0])
