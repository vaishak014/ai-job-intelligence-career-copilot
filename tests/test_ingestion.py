from app.ingest_jobs import ingest_jobs
from app.sources.json_source import JSONJobSource
from app.sources.factory import create_job_source
from app.database import get_connection
from app.database_jobs import (
    insert_job,
    mark_missing_jobs_inactive
)
from app.job_loader import generate_job_fingerprint


def get_test_source():
    return JSONJobSource("data/jobs.json")


def test_ingestion_updates_existing_jobs():
    results = ingest_jobs(get_test_source())

    assert results["inserted"] == 0
    assert results["updated"] == 3
    assert results["skipped"] == 0
    assert results["failed"] == 0


def test_missing_job_is_marked_inactive():

    test_jobs = [
        {
            "job_id": None,
            "title": "Temporary Inactive Test Job 1",
            "company": "Test Company",
            "location": "Bangalore, India",
            "description": "Temporary test job 1.",
            "salary": None,
            "salary_lpa": None,
            "application_status": "Not Applied",
            "application_date": None,
            "application_notes": "",
            "extracted_skills": [],
            "source": "test",
            "source_url": (
                "https://example.com/test-inactive-1"
            ),
            "is_active": True
        },
        {
            "job_id": None,
            "title": "Temporary Inactive Test Job 2",
            "company": "Test Company",
            "location": "Bangalore, India",
            "description": "Temporary test job 2.",
            "salary": None,
            "salary_lpa": None,
            "application_status": "Not Applied",
            "application_date": None,
            "application_notes": "",
            "extracted_skills": [],
            "source": "test",
            "source_url": (
                "https://example.com/test-inactive-2"
            ),
            "is_active": True
        },
        {
            "job_id": None,
            "title": "Temporary Inactive Test Job 3",
            "company": "Test Company",
            "location": "Bangalore, India",
            "description": "Temporary test job 3.",
            "salary": None,
            "salary_lpa": None,
            "application_status": "Not Applied",
            "application_date": None,
            "application_notes": "",
            "extracted_skills": [],
            "source": "test",
            "source_url": (
                "https://example.com/test-inactive-3"
            ),
            "is_active": True
        }
    ]

    for job in test_jobs:
        job["job_fingerprint"] = (
            generate_job_fingerprint(job)
        )

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM jobs
                WHERE source = 'test'
                """
            )

        connection.commit()

        for job in test_jobs:
            result = insert_job(job)
            assert result == "inserted"

        connection.commit()

        deactivated = mark_missing_jobs_inactive(
            [
                {
                    "job_fingerprint":
                        test_jobs[0]["job_fingerprint"]
                },
                {
                    "job_fingerprint":
                        test_jobs[1]["job_fingerprint"]
                }
            ],
            source="test"
        )

        assert deactivated == 1

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT is_active
                FROM jobs
                WHERE source_url = %s
                """,
                (test_jobs[2]["source_url"],)
            )

            result = cursor.fetchone()

        assert result is not None
        assert result[0] is False

    finally:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM jobs
                WHERE source = 'test'
                """
            )

        connection.commit()
        connection.close()


def test_csv_ingestion_pipeline():

    source = create_job_source(
        "csv",
        file_path="data/jobs.csv"
    )

    results = ingest_jobs(
        source,
        "csv"
    )

    assert results["report"]["source_type"] == "csv"
    assert results["report"]["raw_jobs"] == 3
    assert results["quality_report"]["quality_rate"] == 100.0


def test_source_aware_deactivation_does_not_affect_other_sources():

    test_url = (
        "https://example.com/source-isolation-test"
    )

    test_job = {
        "job_id": None,
        "title": "Source Isolation Test Job",
        "company": "Source Isolation Company",
        "location": "Bangalore, India",
        "description": "Temporary source isolation test.",
        "salary": None,
        "salary_lpa": None,
        "application_status": "Not Applied",
        "application_date": None,
        "application_notes": "",
        "extracted_skills": [],
        "source": "test_other",
        "source_url": test_url,
        "is_active": True
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
                (test_url,)
            )

        connection.commit()

        result = insert_job(test_job)

        assert result == "inserted"

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT is_active
                FROM jobs
                WHERE source_url = %s
                """,
                (test_url,)
            )

            before = cursor.fetchone()

        assert before is not None
        assert before[0] is True

        deactivated = mark_missing_jobs_inactive(
            [],
            source="hopin"
        )

        assert deactivated == 0

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT is_active
                FROM jobs
                WHERE source_url = %s
                """,
                (test_url,)
            )

            after = cursor.fetchone()

        assert after is not None
        assert after[0] is True

    finally:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM jobs
                WHERE source_url = %s
                """,
                (test_url,)
            )

        connection.commit()
        connection.close()


def test_source_aware_deactivation_deactivates_missing_hopin_job():

    test_url = (
        "https://example.com/temp-hopin-job"
    )

    test_job = {
        "job_id": None,
        "title": "Temporary Hopin Job",
        "company": "Temporary Hopin Company",
        "location": "Bangalore, India",
        "description": "Temporary test job.",
        "salary": None,
        "salary_lpa": None,
        "application_status": "Not Applied",
        "application_date": None,
        "application_notes": "",
        "extracted_skills": [],
        "source": "hopin",
        "source_url": test_url,
        "is_active": True
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
                (test_url,)
            )

        connection.commit()

        result = insert_job(test_job)

        assert result == "inserted"

        deactivated = mark_missing_jobs_inactive(
            [
                {
                    "job_fingerprint":
                        test_job["job_fingerprint"]
                }
            ],
            source="hopin"
        )

        assert deactivated == 0

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT is_active
                FROM jobs
                WHERE source_url = %s
                """,
                (test_url,)
            )

            row = cursor.fetchone()

        assert row is not None
        assert row[0] is True

        deactivated = mark_missing_jobs_inactive(
            [],
            source="hopin"
        )

        assert deactivated == 1

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT is_active
                FROM jobs
                WHERE source_url = %s
                """,
                (test_url,)
            )

            row = cursor.fetchone()

        assert row is not None
        assert row[0] is False

    finally:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM jobs
                WHERE source_url = %s
                """,
                (test_url,)
            )

        connection.commit()
        connection.close()
