from app.sources.json_source import JSONJobSource


def test_json_job_source():
    source = JSONJobSource("data/jobs.json")

    jobs = source.fetch_jobs()

    assert isinstance(jobs, list)
    assert len(jobs) == 3


def test_json_job_source_returns_job_data():
    source = JSONJobSource("data/jobs.json")

    jobs = source.fetch_jobs()

    assert jobs[0]["title"] == "Python Backend Developer"
    assert jobs[1]["title"] == "Data Analyst"
    assert jobs[2]["title"] == "Machine Learning Engineer"
