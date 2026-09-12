from app.job_quality import (
    validate_job_quality,
    calculate_quality_score,
    filter_quality_jobs
)

from app.job_loader import process_jobs_with_quality_report


def test_valid_job_quality():
    job = {
        "title": "Python Backend Developer",
        "company": "Tech Solutions",
        "location": "Bengaluru",
        "description": "Develop backend APIs using Python."
    }

    result = validate_job_quality(job)

    assert result["is_valid"] is True
    assert result["errors"] == []


def test_missing_company_is_detected():
    job = {
        "title": "Python Backend Developer",
        "company": "",
        "location": "Bengaluru",
        "description": "Develop backend APIs using Python."
    }

    result = validate_job_quality(job)

    assert result["is_valid"] is False
    assert "missing_company" in result["errors"]


def test_quality_score():
    job = {
        "title": "Python Backend Developer",
        "company": "Tech Solutions",
        "location": "Bengaluru",
        "description": "Develop backend APIs using Python."
    }

    score = calculate_quality_score(job)

    assert score == 100.0


def test_quality_score_with_missing_fields():
    job = {
        "title": "Python Backend Developer",
        "company": "",
        "location": "",
        "description": "Develop backend APIs using Python."
    }

    score = calculate_quality_score(job)

    assert score == 50.0


def test_filter_quality_jobs():
    jobs = [
        {
            "title": "Python Backend Developer",
            "company": "Tech Solutions",
            "location": "Bengaluru",
            "description": "Develop backend APIs using Python."
        },
        {
            "title": "Data Analyst",
            "company": "",
            "location": "Mangaluru",
            "description": "Analyze business data."
        }
    ]

    valid_jobs, rejected_jobs = filter_quality_jobs(jobs)

    assert len(valid_jobs) == 1
    assert len(rejected_jobs) == 1
    assert rejected_jobs[0]["errors"] == ["missing_company"]


def test_process_jobs_with_quality_report():
    jobs = [
        {
            "title": "Python Backend Developer",
            "company": "Tech Solutions",
            "location": "Bengaluru",
            "description": "Develop backend APIs using Python."
        },
        {
            "title": "Data Analyst",
            "company": "",
            "location": "Mangaluru",
            "description": "Analyze business data."
        }
    ]

    processed_jobs, rejected_jobs = process_jobs_with_quality_report(
        jobs
    )

    assert len(processed_jobs) == 1
    assert len(rejected_jobs) == 1
    assert rejected_jobs[0]["errors"] == ["missing_company"]
