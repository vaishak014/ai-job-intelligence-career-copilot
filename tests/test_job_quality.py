from app.job_loader import (
    normalize_text,
    generate_job_fingerprint,
    find_duplicate_jobs,
    get_unique_jobs,
    process_jobs
)


def test_normalize_text():
    assert normalize_text("  Python   Developer  ") == "python developer"


def test_same_job_has_same_fingerprint():
    job_1 = {
        "title": "Python Developer",
        "company": "ABC Corp",
        "location": "Bengaluru",
        "description": "Develop Python applications."
    }

    job_2 = {
        "title": "  Python Developer  ",
        "company": "ABC Corp",
        "location": "Bengaluru",
        "description": "Develop   Python applications."
    }

    assert generate_job_fingerprint(job_1) == generate_job_fingerprint(job_2)


def test_different_jobs_have_different_fingerprints():
    job_1 = {
        "title": "Python Developer",
        "company": "ABC Corp",
        "location": "Bengaluru",
        "description": "Develop Python applications."
    }

    job_2 = {
        "title": "Data Analyst",
        "company": "ABC Corp",
        "location": "Bengaluru",
        "description": "Analyze business data."
    }

    assert generate_job_fingerprint(job_1) != generate_job_fingerprint(job_2)


def test_duplicate_jobs_are_detected():
    jobs = [
        {
            "title": "Python Developer",
            "company": "ABC Corp",
            "location": "Bengaluru",
            "description": "Develop Python applications."
        },
        {
            "title": "  Python Developer ",
            "company": "ABC Corp",
            "location": "Bengaluru",
            "description": "Develop   Python applications."
        },
        {
            "title": "Data Analyst",
            "company": "ABC Corp",
            "location": "Bengaluru",
            "description": "Analyze business data."
        }
    ]

    processed_jobs = process_jobs(jobs)

    duplicates = find_duplicate_jobs(processed_jobs)

    assert len(duplicates) == 1


def test_unique_jobs_are_returned():
    jobs = [
        {
            "title": "Python Developer",
            "company": "ABC Corp",
            "location": "Bengaluru",
            "description": "Develop Python applications."
        },
        {
            "title": "Python Developer",
            "company": "ABC Corp",
            "location": "Bengaluru",
            "description": "Develop Python applications."
        }
    ]

    processed_jobs = process_jobs(jobs)

    unique_jobs = get_unique_jobs(processed_jobs)

    assert len(unique_jobs) == 1
