from app.database import get_connection
from app.job_loader import load_jobs, process_jobs


jobs = process_jobs(
    load_jobs("data/jobs.json")
)

connection = get_connection()

try:
    with connection.cursor() as cursor:
        for job in jobs:
            cursor.execute(
                """
                UPDATE jobs
                SET job_fingerprint = %s
                WHERE job_id = %s
                """,
                (
                    job["job_fingerprint"],
                    job["job_id"]
                )
            )

    connection.commit()

    print("Database fingerprints synchronized.")

finally:
    connection.close()
