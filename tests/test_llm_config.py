import os

from app.llm_config import (
    get_llm_provider,
    get_llm_model,
    get_llm_config
)


def test_default_llm_provider():
    assert get_llm_provider() == "mock"


def test_default_llm_model():
    assert get_llm_model() == "local-development"


def test_llm_config_structure():
    config = get_llm_config()

    assert isinstance(config, dict)
    assert config["provider"] == "mock"
    assert config["model"] == "local-development"


def test_environment_provider_override(monkeypatch):
    monkeypatch.setenv(
        "LLM_PROVIDER",
        "test-provider"
    )

    assert get_llm_provider() == "test-provider"


def test_environment_model_override(monkeypatch):
    monkeypatch.setenv(
        "LLM_MODEL",
        "test-model"
    )

    assert get_llm_model() == "test-model"
