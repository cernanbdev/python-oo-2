"""The boundary between our application and the outside world.

Only this module knows that an AI provider exists. models.py never imports it,
and cli.py only ever sees `AIClient`. Swapping providers is a change here and
nowhere else.
"""

import os

try:
    import anthropic
except ImportError:  # the rest of the app still runs without the SDK installed
    anthropic = None

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

MODEL = "claude-opus-5"

SYSTEM_PROMPT = (
    "You are an assistant to a book publisher. "
    "Write short, concrete, plain-language publishing briefs. "
    "No preamble, no markdown headings, under 150 words."
)


class AIServiceError(Exception):
    """One error type for every way the outside world can let us down."""


# TODO (1:05 build): AIClient.
#
# Both backends below already have a .generate(prompt) method. Write the one
# class the rest of the app depends on, so nothing outside this file has to
# know which backend is in play or how it fails.
#
#   class AIClient:
#       def __init__(self, backend): ...
#       def generate(self, prompt): ...   # normalize failures to AIServiceError


class EchoBackend:
    """Offline stand-in so the app is demo-able with no API key and no network."""

    def generate(self, prompt):
        return (
            "[offline sample brief]\n"
            "This author's list is a strong fit for our literary and speculative "
            "imprints. Recommend a paperback reissue in Q3 with a unified cover "
            "treatment across the backlist.\n\n"
            f"(Generated from a {len(prompt)}-character prompt. "
            "Set ANTHROPIC_API_KEY for real output.)"
        )


class AnthropicBackend:
    """Talks to the real Claude API. The only file that imports `anthropic`."""

    def __init__(self, api_key=None, model=MODEL):
        if anthropic is None:
            raise AIServiceError(
                "The `anthropic` package is not installed. Run: pip install anthropic"
            )

        self.client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()
        self.model = model

    def generate(self, prompt):
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.RateLimitError as error:
            raise AIServiceError("Rate limited by the API. Try again shortly.") from error
        except anthropic.APIStatusError as error:
            raise AIServiceError(f"The API returned {error.status_code}.") from error
        except anthropic.APIConnectionError as error:
            raise AIServiceError("Could not reach the API. Check your connection.") from error

        if response.stop_reason == "refusal":
            raise AIServiceError("The model declined to answer that prompt.")

        return "\n".join(
            block.text for block in response.content if block.type == "text"
        ).strip()


def build_ai_client():
    """Pick a backend once, at startup, and hand back one AIClient."""
    load_dotenv()

    # TODO (1:05 build): return an AIClient wrapping AnthropicBackend() when
    # ANTHROPIC_API_KEY is set, and EchoBackend() otherwise.
    raise NotImplementedError("build_ai_client is the 1:05 build")


def build_author_brief_prompt(author):
    """Turn domain objects into text. Prompt wording is service-layer detail."""
    titles = [book.title for book in author.books()]
    catalog = ", ".join(titles) if titles else "no books under contract yet"

    return (
        "Write a short publishing brief.\n"
        f"Author: {author.name}\n"
        f"Books: {catalog}\n"
    )
