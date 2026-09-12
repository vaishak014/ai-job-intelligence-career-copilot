import os


DEFAULT_PROVIDER = "mock"
DEFAULT_MODEL = "local-development"


def get_llm_provider():
    return os.getenv(
        "LLM_PROVIDER",
        DEFAULT_PROVIDER
    )


def get_llm_model():
    return os.getenv(
        "LLM_MODEL",
        DEFAULT_MODEL
    )


def get_llm_config():
    return {
        "provider": get_llm_provider(),
        "model": get_llm_model()
    }
