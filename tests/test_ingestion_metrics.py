from app.ingestion_metrics import build_ingestion_report


def test_ingestion_report():
    results = {
        "inserted": 1,
        "updated": 2,
        "skipped": 0,
        "failed": 0
    }

    report = build_ingestion_report(
        "json",
        3,
        3,
        results,
        0
    )

    assert report["source_type"] == "json"
    assert report["raw_jobs"] == 3
    assert report["valid_jobs"] == 3
    assert report["invalid_jobs"] == 0
    assert report["inserted"] == 1
    assert report["updated"] == 2
    assert report["success_rate"] == 100.0


def test_ingestion_report_with_invalid_jobs():
    results = {
        "inserted": 1,
        "updated": 0,
        "skipped": 0,
        "failed": 0
    }

    report = build_ingestion_report(
        "json",
        4,
        2,
        results,
        0
    )

    assert report["raw_jobs"] == 4
    assert report["valid_jobs"] == 2
    assert report["invalid_jobs"] == 2
    assert report["success_rate"] == 25.0
