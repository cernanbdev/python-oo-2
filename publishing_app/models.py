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
        # TODO (0:45 build): every Contract in Contract.all whose book is self.
        raise NotImplementedError("Book.contracts is the 0:45 build")

    def authors(self):
        # TODO (0:45 build): the author on each of this book's contracts.
        raise NotImplementedError("Book.authors is the 0:45 build")

    def __repr__(self):
        return f"<Book {self.title}>"


class Author:
    """An author may write many books, through many contracts."""

    all = []

    def __init__(self, name):
        self.name = name
        Author.all.append(self)

    def contracts(self):
        # TODO (0:45 build): every Contract in Contract.all whose author is self.
        # You wrote this in demos/02. Now write it where it belongs.
        raise NotImplementedError("Author.contracts is the 0:45 build")

    def books(self):
        # TODO (0:45 build): the book on each of this author's contracts.
        raise NotImplementedError("Author.books is the 0:45 build")

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
