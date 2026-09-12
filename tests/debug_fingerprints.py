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
                SELECT job_id
                FROM jobs
                WHERE job_fingerprint = %s
                """,
                (job["job_fingerprint"],)
            )

            result = cursor.fetchone()

            print(
                "Python job:",
                job["job_id"],
                "DB match:",
                result
            )
finally:
    connection.close()
