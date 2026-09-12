from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Base interface for all LLM providers.

    Every provider must implement the generate()
    method with the same interface.
    """

    @abstractmethod
    def generate(
        self,
        system_prompt,
        candidate_prompt
    ):
        """
        Generate a response from the LLM provider.
        """
        raise NotImplementedError
