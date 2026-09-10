"""Domain models for the publishing app.

Everything about *how* publishers, books, authors and contracts relate to one
another lives in this file. The CLI is allowed to ask these objects questions.
It is not allowed to rebuild the relationships for itself.
"""


class Publisher:
    """One publisher has many books."""

    all = []

    def __init__(self, name):
        self.name = name
        self.books = []
        Publisher.all.append(self)

    def authors(self):
        """Every author under contract for one of this publisher's books."""
        found = []

        for book in self.books:
            for author in book.authors():
                if author not in found:
                    found.append(author)

        return found

    def __repr__(self):
        return f"<Publisher {self.name}>"


class Book:
    """A book belongs to one publisher and may have many authors."""

    all = []

    def __init__(self, title, publisher):
        self.title = title

        # One-to-many. The single reference lives on the "many" side, and the
        # book adds itself to the publisher's list so both directions work.
        self.publisher = publisher
        publisher.books.append(self)

        Book.all.append(self)

    def contracts(self):
        return [
            contract
            for contract in Contract.all
            if contract.book == self
        ]

    def authors(self):
        return [contract.author for contract in self.contracts()]

    def __repr__(self):
        return f"<Book {self.title}>"


class Author:
    """An author may write many books, through many contracts."""

    all = []

    def __init__(self, name):
        self.name = name
        Author.all.append(self)

    def contracts(self):
        return [
            contract
            for contract in Contract.all
            if contract.author == self
        ]

    def books(self):
        return [contract.book for contract in self.contracts()]

    # TODO (1:17 challenge): add sign(self, book, royalty) so creating a
    # contract reads as something the author does.

    def __repr__(self):
        return f"<Author {self.name}>"


class Contract:
    """The association object that joins one author to one book.

    Because the relationship itself is an object, it can carry data of its own
    (here, the royalty percentage). That is the payoff for the extra class.
    """

    all = []

    def __init__(self, author, book, royalty):
        # TODO (1:17 challenge): royalty must be a number between 0 and 100.
        # Ask the room where that rule belongs before you write it.

        self.author = author
        self.book = book
        self.royalty = royalty

        Contract.all.append(self)

    def __repr__(self):
        return f"<Contract {self.author.name} / {self.book.title} @ {self.royalty}%>"
