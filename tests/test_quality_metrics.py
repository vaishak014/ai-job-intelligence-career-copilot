from app.quality_metrics import build_quality_report


def test_quality_report():
    raw_jobs = [
        {"title": "Job 1"},
        {"title": "Job 2"},
        {"title": "Job 3"},
        {"title": "Job 4"}
    ]

    processed_jobs = [
        {"title": "Job 1"},
        {"title": "Job 2"},
        {"title": "Job 3"}
    ]

    rejected_jobs = [
        {
            "job": {"title": "Job 4"},
            "errors": ["missing_company"]
        }
    ]

    report = build_quality_report(
        raw_jobs,
        processed_jobs,
        rejected_jobs
    )

    assert report["raw_jobs"] == 4
    assert report["valid_jobs"] == 3
    assert report["rejected_jobs"] == 1
    assert report["quality_rate"] == 75.0
    assert report["rejection_reasons"] == {
        "missing_company": 1
    }


def test_multiple_rejection_reasons():
    raw_jobs = [
        {"title": "Job 1"},
        {"title": "Job 2"},
        {"title": "Job 3"}
    ]

    processed_jobs = [
        {"title": "Job 1"}
    ]

    rejected_jobs = [
        {
            "job": {"title": "Job 2"},
            "errors": [
                "missing_company",
                "missing_location"
            ]
        },
        {
            "job": {"title": "Job 3"},
            "errors": ["missing_company"]
        }
    ]

    report = build_quality_report(
        raw_jobs,
        processed_jobs,
        rejected_jobs
    )

    assert report["rejected_jobs"] == 2
    assert report["quality_rate"] == 33.33

    assert report["rejection_reasons"] == {
        "missing_company": 2,
        "missing_location": 1
    }
