from app.database import get_connection
from app.database_jobs import insert_job
from app.job_loader import generate_job_fingerprint


TEST_SOURCE_URL = (
    "https://example.com/metadata-test-job"
)


def test_source_metadata_persistence():

    test_job = {
        "job_id": None,
        "title": "Metadata Persistence Test Job",
        "company": "Metadata Test Company",
        "location": "Bangalore, India",
        "description": (
            "Python backend development "
            "with FastAPI and PostgreSQL."
        ),
        "salary": "6 LPA",
        "salary_lpa": 6.0,
        "application_status": "Not Applied",
        "application_date": None,
        "application_notes": "",
        "extracted_skills": [],
        "source": "hopin",
        "source_url": TEST_SOURCE_URL,
        "is_active": True,

        "source_job_id": "metadata-test-001",
        "source_is_unofficial": True,
        "source_posted_at": "2026-09-09T10:30:00",
        "source_posted_days": 0,
        "source_industry": "Technology",
        "source_role_type": "Software Engineering",
        "source_work_type": "On-site",
        "source_criteria": [
            "Python",
            "FastAPI",
            "PostgreSQL"
        ]
    }

    test_job["job_fingerprint"] = (
        generate_job_fingerprint(test_job)
    )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM jobs
                WHERE source_url = %s
                """,
                (TEST_SOURCE_URL,)
            )

        connection.commit()

        result = insert_job(test_job)

        assert result == "inserted"

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT job_id
                FROM jobs
                WHERE source_url = %s
                """,
                (TEST_SOURCE_URL,)
            )

            job_row = cursor.fetchone()

        assert job_row is not None

        job_id = job_row[0]

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    source,
                    source_job_id,
                    is_unofficial,
                    posted_at,
                    posted_days,
                    industry,
                    role_type,
                    work_type,
                    criteria
                FROM job_source_metadata
                WHERE job_id = %s
                AND source = 'hopin'
                """,
                (job_id,)
            )

            metadata = cursor.fetchone()

        assert metadata is not None

        assert metadata[0] == "hopin"
        assert metadata[1] == "metadata-test-001"
        assert metadata[2] is True

        assert metadata[3] is not None
        assert metadata[3].isoformat() == (
            "2026-09-09T10:30:00"
        )

        assert metadata[4] == 0
        assert metadata[5] == "Technology"
        assert metadata[6] == "Software Engineering"
        assert metadata[7] == "On-site"

        assert metadata[8] == [
            "Python",
            "FastAPI",
            "PostgreSQL"
        ]

    finally:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM jobs
                WHERE source_url = %s
                """,
                (TEST_SOURCE_URL,)
            )

        connection.commit()
        connection.close()
