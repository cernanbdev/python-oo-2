"""Load the starting objects from data/books.json.

Keeping the sample data in a file (instead of hard-coding it in models.py or
cli.py) is the Module 6 point: code in one place, data in another.
"""

import json
from pathlib import Path

from solution.models import Author, Book, Contract, Publisher

DATA_FILE = Path(__file__).parent / "data" / "books.json"

MODELS = (Publisher, Book, Author, Contract)


def reset():
    """Empty every `all` list. Tests and reloads depend on this."""
    for model in MODELS:
        model.all.clear()


def load_data(path=DATA_FILE):
    """Build Publisher, Book, Author and Contract objects from JSON."""
    reset()

    raw = json.loads(Path(path).read_text(encoding="utf-8"))

    publishers = {name: Publisher(name) for name in raw["publishers"]}
    authors = {name: Author(name) for name in raw["authors"]}

    books = {
        entry["title"]: Book(entry["title"], publishers[entry["publisher"]])
        for entry in raw["books"]
    }

    for entry in raw["contracts"]:
        Contract(
            authors[entry["author"]],
            books[entry["book"]],
            entry["royalty"],
        )
