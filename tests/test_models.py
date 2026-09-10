"""The relationship rules, tested directly against the models."""

import pytest

from solution.models import Author, Book, Contract, Publisher


def find(model, attribute, value):
    return next(item for item in model.all if getattr(item, attribute) == value)


def test_book_knows_its_publisher():
    kindred = find(Book, "title", "Kindred")

    assert kindred.publisher.name == "Doubleday"


def test_publisher_knows_its_books():
    doubleday = find(Publisher, "name", "Doubleday")

    assert [book.title for book in doubleday.books] == [
        "Kindred",
        "Parable of the Sower",
    ]


def test_author_reaches_books_through_contracts():
    butler = find(Author, "name", "Octavia Butler")

    assert [book.title for book in butler.books()] == [
        "Kindred",
        "Parable of the Sower",
    ]


def test_book_reaches_authors_through_contracts():
    """The many-to-many case: one book, two authors."""
    good_omens = find(Book, "title", "Good Omens")

    assert [author.name for author in good_omens.authors()] == [
        "Neil Gaiman",
        "Terry Pratchett",
    ]


def test_author_with_no_contracts_has_no_books():
    chiang = find(Author, "name", "Ted Chiang")

    assert chiang.books() == []


def test_publisher_reaches_authors_across_books_without_duplicates():
    knopf = find(Publisher, "name", "Knopf")

    assert [author.name for author in knopf.authors()] == ["Toni Morrison"]


def test_signing_creates_the_contract():
    chiang = find(Author, "name", "Ted Chiang")
    exhalation = find(Book, "title", "Exhalation")

    contract = chiang.sign(exhalation, 11.0)

    assert contract in Contract.all
    assert chiang.books() == [exhalation]
    assert exhalation.authors() == [chiang]


@pytest.mark.parametrize("royalty", [0, 12.5, 100])
def test_royalty_accepts_the_full_valid_range(royalty):
    chiang = find(Author, "name", "Ted Chiang")
    exhalation = find(Book, "title", "Exhalation")

    assert chiang.sign(exhalation, royalty).royalty == royalty


@pytest.mark.parametrize("royalty", [-0.1, 101, 1000])
def test_royalty_outside_the_range_is_rejected(royalty):
    chiang = find(Author, "name", "Ted Chiang")
    exhalation = find(Book, "title", "Exhalation")

    with pytest.raises(ValueError):
        chiang.sign(exhalation, royalty)


@pytest.mark.parametrize("royalty", ["12.5", None, True])
def test_royalty_must_be_a_number(royalty):
    chiang = find(Author, "name", "Ted Chiang")
    exhalation = find(Book, "title", "Exhalation")

    with pytest.raises(TypeError):
        chiang.sign(exhalation, royalty)


def test_a_rejected_contract_is_not_recorded():
    chiang = find(Author, "name", "Ted Chiang")
    exhalation = find(Book, "title", "Exhalation")
    before = len(Contract.all)

    with pytest.raises(ValueError):
        chiang.sign(exhalation, 500)

    assert len(Contract.all) == before
