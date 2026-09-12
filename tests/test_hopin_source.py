from unittest.mock import patch, Mock

import requests

from app.sources.hopin_source import HopinSource


def test_hopin_source_fetch_jobs():
    mock_response = Mock()

    mock_response.json.return_value = {
        "jobs": [
            {
                "id": "job-1",
                "title": "Python Developer",
                "company": "Test Company",
                "location": "Bangalore, India"
            },
            {
                "id": "job-2",
                "title": "Data Analyst",
                "company": "Analytics Corp",
                "location": "Mangalore, India"
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "app.sources.hopin_source.requests.get",
        return_value=mock_response
    ) as mock_get:

        source = HopinSource(
            industry="Technology"
        )

        jobs = source.fetch_jobs()

    assert len(jobs) == 2
    assert jobs[0]["title"] == "Python Developer"
    assert jobs[1]["company"] == "Analytics Corp"

    mock_get.assert_called_once()

    request_params = mock_get.call_args.kwargs["params"]

    assert request_params["industry"] == "Technology"
    assert request_params["is_unofficial"] == "true"


def test_hopin_source_handles_request_error():

    with patch(
        "app.sources.hopin_source.requests.get",
        side_effect=requests.RequestException(
            "Network error"
        )
    ):

        source = HopinSource(
            industry="Technology"
        )

        jobs = source.fetch_jobs()

    assert jobs == []


def test_hopin_source_handles_invalid_response():

    mock_response = Mock()

    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "jobs": "invalid"
    }

    with patch(
        "app.sources.hopin_source.requests.get",
        return_value=mock_response
    ):

        source = HopinSource(
            industry="Technology"
        )

        jobs = source.fetch_jobs()

    assert jobs == []
