from app.database_jobs import get_all_jobs


jobs = get_all_jobs()

print("Jobs:", len(jobs))

for job in jobs:
    if job.get("source") == "hopin":
        description = job.get("description", "")

        description = description.replace(
            "\n",
            " "
        )

        print(
            job["job_id"],
            "|",
            job["title"],
            "|",
            description[:500]
        )
