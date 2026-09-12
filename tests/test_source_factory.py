import pytest

from app.sources.factory import create_job_source


def test_create_json_source():
    source = create_job_source(
        "json",
        file_path="data/jobs.json"
    )

    jobs = source.fetch_jobs()

    assert len(jobs) == 3


def test_unsupported_source_raises_error():
    with pytest.raises(ValueError):
        create_job_source("unsupported")


def test_create_csv_job_source():
    source = create_job_source(
        "csv",
        file_path="data/jobs.csv"
    )

    assert source.__class__.__name__ == "CSVJobSource"


def test_create_api_job_source():
    source = create_job_source(
        "api",
        url="https://example.com/jobs"
    )

    assert source.__class__.__name__ == "APIJobSource"


def test_create_hopin_source():
    from app.sources.factory import create_job_source
    from app.sources.hopin_source import HopinSource

    source = create_job_source(
        "hopin",
        industry="Technology",
        location="Bangalore, India",
        work_type="On-site",
        role_type="Software Engineering"
    )

    assert isinstance(source, HopinSource)
    assert source.industry == "Technology"
    assert source.location == "Bangalore, India"
    assert source.work_type == "On-site"
    assert source.role_type == "Software Engineering"
    assert source.is_unofficial is True
