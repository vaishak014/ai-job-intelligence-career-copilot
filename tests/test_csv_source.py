from app.sources.csv_source import CSVJobSource


def test_csv_job_source():
    source = CSVJobSource(
        "data/jobs.csv"
    )

    jobs = source.fetch_jobs()

    assert len(jobs) == 3
    assert jobs[0]["title"] == "Python Backend Developer"
    assert jobs[0]["company"] == "Cloud Systems"
    assert jobs[1]["location"] == "Mangaluru"


def test_csv_job_source_missing_file():
    source = CSVJobSource(
        "data/nonexistent_jobs.csv"
    )

    jobs = source.fetch_jobs()

    assert jobs == []
