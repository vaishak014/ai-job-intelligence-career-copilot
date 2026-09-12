from unittest.mock import patch, Mock

from app.database import get_connection
from app.ingest_jobs import ingest_jobs
from app.sources.hopin_source import HopinSource


TEST_SOURCE_URL = (
    "https://example.com/hopin-test-001"
)


def cleanup_test_job():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM jobs
                WHERE source = 'hopin'
                AND source_url = %s
                """,
                (TEST_SOURCE_URL,)
            )

        connection.commit()

    finally:
        connection.close()


def test_hopin_ingestion_pipeline():

    cleanup_test_job()

    mock_response = Mock()

    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = {
        "jobs": [
            {
                "id": "hopin-test-001",
                "company": "Hopin Test Company",
                "title": "Python Backend Developer",
                "description": (
                    "Python backend development "
                    "with FastAPI and PostgreSQL."
                ),
                "salary": None,
                "ctc_amount": "6 LPA",
                "work_type": "On-site",
                "location": "Bengaluru, India",
                "industry": "Technology",
                "role_type": "Software Engineering",
                "is_active": True,
                "is_unofficial": True,
                "apply_url": TEST_SOURCE_URL,
                "posted_days": 1,
                "criteria": [
                    "Python",
                    "FastAPI",
                    "PostgreSQL"
                ]
            }
        ]
    }

    try:
        with patch(
            "app.sources.hopin_source.requests.get",
            return_value=mock_response
        ):

            source = HopinSource(
                industry="Technology"
            )

            result = ingest_jobs(
                source,
                source_type="hopin"
            )

        assert result["inserted"] >= 1
        assert result["failed"] == 0
        assert result["report"]["source_type"] == "hopin"
        assert result["quality_report"]["raw_jobs"] == 1
        assert result["quality_report"]["valid_jobs"] == 1

    finally:
        cleanup_test_job()
