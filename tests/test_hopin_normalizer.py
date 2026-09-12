from app.sources.hopin_normalizer import (
    normalize_hopin_job,
    normalize_hopin_jobs
)


def test_normalize_hopin_job():

    raw_job = {
        "id": "08e33b19-7324-4ae6-870c-bfcb077b0a20",
        "company": "KPIT Technologies",
        "title": "Associate Software Engineer",
        "title_clean": "Associate Software Engineer",
        "description": "Technology / Software Engineering",
        "salary": None,
        "ctc": None,
        "ctc_amount": "Competitive",
        "work_type": "On-site",
        "location": (
            "Pune, India | Bengaluru, India | Kochi, India"
        ),
        "posted_at": "2026-09-03T11:35:11",
        "industry": "Technology",
        "role_type": "Software Engineering",
        "is_active": True,
        "is_unofficial": True,
        "apply_url": "https://example.com/apply",
        "criteria": [
            "Bachelor's degree",
            "Programming knowledge"
        ],
        "posted_days": 6
    }

    job = normalize_hopin_job(raw_job)

    assert job["job_id"] is None
    assert job["source_job_id"] == (
        "08e33b19-7324-4ae6-870c-bfcb077b0a20"
    )

    assert job["title"] == "Associate Software Engineer"
    assert job["company"] == "KPIT Technologies"

    assert "Bangalore, India" in job["location"]
    assert "Bengaluru, India" not in job["location"]

    assert job["salary"] == "Competitive"

    assert job["source"] == "hopin"
    assert job["source_url"] == (
        "https://example.com/apply"
    )

    assert job["source_is_unofficial"] is True
    assert job["source_industry"] == "Technology"
    assert job["source_role_type"] == (
        "Software Engineering"
    )

    assert len(job["source_criteria"]) == 2


def test_normalize_hopin_job_uses_apply_form_url():

    raw_job = {
        "id": "job-2",
        "company": "Test Company",
        "title": "Python Developer",
        "location": "Bengaluru, India",
        "description": "Python development",
        "apply_form_url": "https://example.com/form"
    }

    job = normalize_hopin_job(raw_job)

    assert job["source_url"] == (
        "https://example.com/form"
    )


def test_normalize_hopin_job_handles_missing_optional_fields():

    raw_job = {
        "id": "job-3",
        "company": "Test Company",
        "title": "Data Analyst",
        "location": "Bangalore, India",
        "description": "Analyze data"
    }

    job = normalize_hopin_job(raw_job)

    assert job["job_id"] is None
    assert job["source_job_id"] == "job-3"
    assert job["salary"] is None
    assert job["source_url"] is None
    assert job["source_criteria"] == []


def test_normalize_hopin_jobs():

    raw_jobs = [
        {
            "id": "job-1",
            "company": "Company A",
            "title": "Python Developer",
            "location": "Bangalore, India",
            "description": "Python"
        },
        {
            "id": "job-2",
            "company": "Company B",
            "title": "Data Analyst",
            "location": "Mangaluru, India",
            "description": "Data analysis"
        }
    ]

    jobs = normalize_hopin_jobs(raw_jobs)

    assert len(jobs) == 2
    assert jobs[0]["source_job_id"] == "job-1"
    assert jobs[1]["source_job_id"] == "job-2"
