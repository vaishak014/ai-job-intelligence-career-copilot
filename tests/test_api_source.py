from app.sources.api_source import APIJobSource


class MockResponse:

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "jobs": [
                {
                    "title": "Python Developer",
                    "company": "Test Company",
                    "location": "Bengaluru",
                    "description": "Build Python applications."
                },
                {
                    "title": "Data Analyst",
                    "company": "Analytics Company",
                    "location": "Mangaluru",
                    "description": "Analyze business data."
                }
            ]
        }


def test_api_job_source(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(
        "app.sources.api_source.requests.get",
        mock_get
    )

    source = APIJobSource(
        "https://example.com/jobs"
    )

    jobs = source.fetch_jobs()

    assert len(jobs) == 2
    assert jobs[0]["title"] == "Python Developer"
    assert jobs[1]["company"] == "Analytics Company"
