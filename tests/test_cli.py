"""The CLI, tested by feeding it keystrokes and reading what it printed.

This is only possible because the CLI functions are small and do one job. It is
the practical payoff of separating models, CLI and services.
"""

import pytest

from publishing_app import cli
from publishing_app.models import Author, Contract
from publishing_app.services import AIClient, AIServiceError, EchoBackend


@pytest.fixture
def keystrokes(monkeypatch):
    """Queue up what the user 'types'."""

    def press(*answers):
        queued = iter(answers)
        monkeypatch.setattr("builtins.input", lambda *args: next(queued))

    return press


def test_view_an_authors_books(keystrokes, capsys):
    keystrokes("1")  # Octavia Butler

    cli.show_author_books()

    output = capsys.readouterr().out
    assert "Books by Octavia Butler" in output
    assert "- Kindred" in output
    assert "- Parable of the Sower" in output


def test_non_numeric_choice_is_reported_not_raised(keystrokes, capsys):
    keystrokes("hello")

    cli.show_author_books()

    assert "Please enter a number." in capsys.readouterr().out


@pytest.mark.parametrize("choice", ["0", "27", "-1"])
def test_out_of_range_choice_is_reported_not_raised(keystrokes, capsys, choice):
    keystrokes(choice)

    cli.show_author_books()

    assert "not one of the options" in capsys.readouterr().out


def test_author_with_no_books_gets_a_real_message(keystrokes, capsys):
    keystrokes("8")  # Ted Chiang

    cli.show_author_books()

    assert "no books under contract yet" in capsys.readouterr().out


def test_creating_a_contract_records_it(keystrokes, capsys):
    before = len(Contract.all)
    keystrokes("8", "11", "12.5")  # Ted Chiang, Exhalation, 12.5%

    cli.create_contract()

    assert len(Contract.all) == before + 1
    assert "Contract created" in capsys.readouterr().out

    chiang = next(a for a in Author.all if a.name == "Ted Chiang")
    assert [book.title for book in chiang.books()] == ["Exhalation"]


def test_cli_reports_a_royalty_the_model_rejected(keystrokes, capsys):
    before = len(Contract.all)
    keystrokes("8", "11", "150")

    cli.create_contract()

    assert len(Contract.all) == before
    assert "between 0 and 100" in capsys.readouterr().out


def test_brief_prints_whatever_the_service_returns(keystrokes, capsys):
    keystrokes("1")

    cli.generate_author_brief(AIClient(EchoBackend()))

    assert "brief" in capsys.readouterr().out


def test_brief_failure_does_not_crash_the_cli(keystrokes, capsys):
    class Broken:
        def generate(self, prompt):
            raise AIServiceError("service is down")

    keystrokes("1")

    cli.generate_author_brief(AIClient(Broken()))

    assert "Could not generate a brief. service is down" in capsys.readouterr().out
