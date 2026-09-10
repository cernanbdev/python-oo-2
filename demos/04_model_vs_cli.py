"""0:28 - Where should relationship logic live?

Same printed output, two very different designs. Show the first version, ask
which one should know how authors and books are connected, then show the
second.

Run it:  python demos/04_model_vs_cli.py
"""


class Contract:
    all = []

    def __init__(self, author, book, royalty):
        self.author = author
        self.book = book
        self.royalty = royalty
        Contract.all.append(self)


class Author:
    def __init__(self, name):
        self.name = name

    def contracts(self):
        return [c for c in Contract.all if c.author == self]

    def books(self):
        return [c.book for c in self.contracts()]


class Book:
    def __init__(self, title):
        self.title = title


def show_author_books_bad(author):
    books = []

    for contract in Contract.all:
        if contract.author == author:
            books.append(contract.book)

    for book in books:
        print(f"- {book.title}")


# The CLI asks a question. The model answers it.
def show_author_books_better(author):
    for book in author.books():
        print(f"- {book.title}")


butler = Author("Octavia Butler")
Contract(butler, Book("Kindred"), 12.5)
Contract(butler, Book("Parable of the Sower"), 14.0)

print("Version A (CLI knows the relationship):")
show_author_books_bad(butler)

print("\nVersion B (model knows the relationship):")
show_author_books_better(butler)

# The model should know the relationship.
# The CLI should know how to interact with the user.
