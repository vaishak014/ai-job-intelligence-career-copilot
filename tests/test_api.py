from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_get_jobs():
    response = client.get("/jobs")

    assert response.status_code == 200

    jobs = response.json()

    assert len(jobs) >= 3

    job_ids = [
        job["job_id"]
        for job in jobs
    ]

    assert 1 in job_ids


def test_search_jobs():
    response = client.get(
        "/jobs/search",
        params={"title": "Python"}
    )

    assert response.status_code == 200

    jobs = response.json()

    assert len(jobs) >= 1
    assert all("python" in job["title"].lower() for job in jobs)


def test_get_job():
    response = client.get("/jobs/1")

    assert response.status_code == 200

    job = response.json()

    assert job["title"] == "Python Backend Developer"


def test_get_non_existing_job():
    response = client.get("/jobs/999")

    assert response.status_code == 404


def test_get_candidate():
    response = client.get("/candidates/1")

    assert response.status_code == 200

    candidate = response.json()

    assert candidate["candidate_id"] == 1


def test_get_candidate_matches():
    response = client.get(
        "/candidates/1/matches"
    )

    assert response.status_code == 200

    matches = response.json()

    assert len(matches) >= 3

    job_ids = [
        match["job_id"]
        for match in matches
    ]

    assert 1 in job_ids
    assert 2 in job_ids
    assert 3 in job_ids

    data_by_job_id = {
        match["job_id"]: match
        for match in matches
    }

    assert data_by_job_id[2]["overall_match"] == 80


def test_get_candidate_intelligence():
    response = client.get(
        "/candidates/1/intelligence"
    )

    assert response.status_code == 200

    intelligence = response.json()

    assert "profile" in intelligence
    assert "recommendations" in intelligence
    assert "skill_gaps" in intelligence
    assert "skill_priorities" in intelligence


def test_application_statistics():
    response = client.get(
        "/applications/statistics"
    )

    assert response.status_code == 200

    statistics = response.json()

    assert statistics["interview"] == 2


def test_invalid_application_status():
    response = client.put(
        "/jobs/1/application-status",
        json={
            "status": "invalid status"
        }
    )

    assert response.status_code == 422


def test_valid_application_status():
    response = client.put(
        "/jobs/1/application-status",
        json={
            "status": "interview"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["application_status"] == "Interview"
