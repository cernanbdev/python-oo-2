"""0:20 - Many-to-many needs a third object.

An author writes many books. A book can have many authors. So where would
author_id go? Nowhere. The relationship needs an object of its own.

Run it:  python demos/02_many_to_many.py
"""


class Contract:
    all = []

    def __init__(self, author, book):
        self.author = author
        self.book = book
        Contract.all.append(self)


class Author:
    def __init__(self, name):
        self.name = name

    def contracts(self):
        return [
            contract
            for contract in Contract.all
            if contract.author == self
        ]

    def books(self):
        return [contract.book for contract in self.contracts()]


class Book:
    def __init__(self, title):
        self.title = title

    def authors(self):
        return [
            contract.author
            for contract in Contract.all
            if contract.book == self
        ]


gaiman = Author("Neil Gaiman")
pratchett = Author("Terry Pratchett")

american_gods = Book("American Gods")
good_omens = Book("Good Omens")

Contract(gaiman, american_gods)
Contract(gaiman, good_omens)
Contract(pratchett, good_omens)

print("Gaiman's books:     ", [book.title for book in gaiman.books()])
print("Good Omens' authors:", [author.name for author in good_omens.authors()])

# Both sides connect many times, and neither class stores the other's id.
