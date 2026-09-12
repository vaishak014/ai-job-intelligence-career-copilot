from app.llm_client import (
    create_llm_client
)


def test_mock_copilot_response():
    client = create_llm_client()

    result = client.generate(
        "You are an AI Career Copilot.",
        "Candidate has Python and SQL skills."
    )

    assert result is not None
    assert result["status"] == "success"
    assert result["provider"] == "mock"
    assert result["response"] is not None
    assert "Career Copilot" in result["response"]
    assert "Python" in result["response"]
