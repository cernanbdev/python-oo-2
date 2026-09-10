"""0:15 - One-to-many: one publisher, many books.

Run it:  python demos/01_one_to_many.py
"""


class Publisher:
    def __init__(self, name):
        self.name = name
        self.books = []


class Book:
    def __init__(self, title, publisher):
        self.title = title
        self.publisher = publisher
        publisher.books.append(self)


penguin = Publisher("Penguin")

book1 = Book("Python Basics", penguin)
book2 = Book("Learning APIs", penguin)

# Two directions, one relationship.
print("From the book: ", book1.publisher.name)
print("From the publisher:", [book.title for book in penguin.books])
