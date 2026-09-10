"""0:25 - Why isn't Contract just annoying extra code?

Because the relationship itself has data. A royalty is not a fact about the
author, and not a fact about the book. It is a fact about the agreement.

Run it:  python demos/03_contract_metadata.py
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

    def total_royalty(self):
        return sum(c.royalty for c in self.contracts())


class Book:
    def __init__(self, title):
        self.title = title


gaiman = Author("Neil Gaiman")
pratchett = Author("Terry Pratchett")
good_omens = Book("Good Omens")

Contract(gaiman, good_omens, 7.5)
Contract(pratchett, good_omens, 7.5)
Contract(gaiman, Book("American Gods"), 15.0)

for contract in Contract.all:
    print(f"{contract.author.name:18} {contract.book.title:16} {contract.royalty}%")

print()
print("Gaiman's combined royalty:", gaiman.total_royalty())

# The same two authors, the same book, different agreements. Only an
# association object can hold that.
