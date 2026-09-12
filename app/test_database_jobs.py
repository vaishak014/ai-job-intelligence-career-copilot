from database_jobs import get_all_jobs


jobs = get_all_jobs()

print("Total jobs in PostgreSQL:", len(jobs))

for job in jobs:
    print()
    print("Job ID:", job["job_id"])
    print("Title:", job["title"])
    print("Company:", job["company"])
    print("Location:", job["location"])
    print("Salary LPA:", job["salary_lpa"])
    print("Application Status:", job["application_status"])
