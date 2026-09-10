"""The service layer, tested without touching the network."""

import pytest

from publishing_app.models import Author
from publishing_app.services import AIClient, AIServiceError, EchoBackend, build_author_brief_prompt


class ExplodingBackend:
    def generate(self, prompt):
        raise RuntimeError("socket closed")


class RecordingBackend:
    def __init__(self):
        self.seen = []

    def generate(self, prompt):
        self.seen.append(prompt)
        return "a brief"


def find_author(name):
    return next(author for author in Author.all if author.name == name)


def test_client_passes_the_prompt_through_to_the_backend():
    backend = RecordingBackend()

    assert AIClient(backend).generate("hello") == "a brief"
    assert backend.seen == ["hello"]


def test_client_turns_any_backend_failure_into_one_error_type():
    """This is the whole reason the wrapper exists."""
    with pytest.raises(AIServiceError):
        AIClient(ExplodingBackend()).generate("hello")


def test_client_does_not_rewrap_its_own_error():
    class AlreadyWrapped:
        def generate(self, prompt):
            raise AIServiceError("rate limited")

    with pytest.raises(AIServiceError, match="rate limited"):
        AIClient(AlreadyWrapped()).generate("hello")


def test_offline_backend_needs_no_key_or_network():
    assert "brief" in AIClient(EchoBackend()).generate("hello")


def test_prompt_is_built_from_the_author_and_their_books():
    prompt = build_author_brief_prompt(find_author("Octavia Butler"))

    assert "Octavia Butler" in prompt
    assert "Kindred" in prompt
    assert "Parable of the Sower" in prompt


def test_prompt_handles_an_author_with_no_books():
    prompt = build_author_brief_prompt(find_author("Ted Chiang"))

    assert "Ted Chiang" in prompt
    assert "no books under contract yet" in prompt
