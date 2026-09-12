import pytest

from app.llm_client import (
    LLMClient,
    create_llm_client,
    generate_mock_response
)


def test_create_llm_client():
    client = create_llm_client()

    assert isinstance(
        client,
        LLMClient
    )

    assert client.provider == "mock"
    assert client.model == "local-development"


def test_llm_client_generate_mock_response():
    client = LLMClient()

    result = client.generate(
        "You are a career assistant.",
        "Help this candidate."
    )

    assert result is not None
    assert result["provider"] == "mock"
    assert result["model"] == "local-development"
    assert (
        result["system_prompt"]
        == "You are a career assistant."
    )
    assert (
        result["candidate_prompt"]
        == "Help this candidate."
    )
    assert result["response"] is not None
    assert (
        "Career Copilot"
        in result["response"]
    )
    assert result["status"] == "success"


def test_generate_mock_response():
    result = generate_mock_response(
        "Candidate has Python skills."
    )

    assert result is not None
    assert len(result) > 0
    assert "Python" in result
    assert "Development Response" in result


def test_llm_client_rejects_empty_system_prompt():
    client = LLMClient()

    with pytest.raises(ValueError):
        client.generate(
            "",
            "Candidate prompt"
        )


def test_llm_client_rejects_empty_candidate_prompt():
    client = LLMClient()

    with pytest.raises(ValueError):
        client.generate(
            "System prompt",
            ""
        )


def test_llm_client_unknown_provider():
    client = LLMClient(
        provider="unknown",
        model="test-model"
    )

    result = client.generate(
        "System prompt",
        "Candidate prompt"
    )

    assert result["provider"] == "unknown"
    assert result["model"] == "test-model"
    assert result["response"] is None
    assert result["status"] == "not_configured"
