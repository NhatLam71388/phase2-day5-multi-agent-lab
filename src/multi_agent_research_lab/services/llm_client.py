"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client."""

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion.

        The default is deterministic and offline-safe for the lab. It records rough
        token estimates so benchmarks can still report cost-related fields.
        """

        system_words = system_prompt.split()
        user_words = user_prompt.split()
        summary = " ".join(user_words[:80])
        content = (
            "Offline completion: "
            f"{summary}. "
            "Use provider-backed completion here when API credentials are configured."
        )
        return LLMResponse(
            content=content,
            input_tokens=len(system_words) + len(user_words),
            output_tokens=len(content.split()),
            cost_usd=0.0,
        )
