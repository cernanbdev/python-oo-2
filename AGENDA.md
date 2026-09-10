# 90-Minute Live Session: From Object Relationships to a Python CLI

## Session Theme

**How do we take related Python objects and turn them into a usable application?**

The session follows one evolving example: a **publishing management CLI**.

Students will move from:

`Python objects -> object relationships -> application modules -> CLI -> external service`

### Learning Goals

By the end of the session, students should be able to:

* Distinguish one-to-many from many-to-many relationships.
* Explain why many-to-many relationships usually require an intermediate/association object.
* Navigate relationships between Python objects.
* Separate models, CLI logic, and service logic into different Python files.
* Map user actions in a CLI to operations on related objects.
* Explain why an external API or AI client should be wrapped in a reusable class rather than scattered throughout an application.

---

# 0:00-0:15 - Technical Q&A

**Framework allocation: ~16%**

Start by opening the floor for questions from Modules 5-7.

Suggested prompt:

> "Before we build anything, what has been confusing this week?
> Object relationships, imports, file structure, pip, CLI loops, external services - all are fair game."

As students ask questions, keep a running list of concepts that come up.

If questions are slow, use these diagnostic questions:

**Object Relationships**

"What is the difference between saying `book.author` and `author.books`?"

"If an author can write many books AND a book can have multiple authors, can we store `author_id` directly on Book?"

"What role does the `Contract` class play in the Book Contracts lab?"

**Imports / Application Structure**

"What happens when Python executes an `import`?"

"Why might we put our classes in `models.py` instead of writing everything in `cli.py`?"

"What does this mean?"

```python
if __name__ == "__main__":
    main()
```

**CLI**

"What should happen if a user enters an invalid menu option?"

"What is the difference between application logic and presentation/user-interface logic?"

**External Services**

"Why might calling an API directly from every CLI function become difficult to maintain?"

Use student responses to identify what needs extra emphasis later in the session.

---

# 0:15-0:30 - Concept Review

## Core Concept: Modeling Relationships Between Objects

Explain that applications rarely contain isolated objects.

Real applications contain relationships:

```text
Customer -> Orders
Department -> Employees
Doctor <-> Patients
Authors <-> Books
```

The important question is:

> **Where does the relationship live, and how do we navigate it?**

---

## Example 1 - Easy: One-to-Many

> Run it: `python demos/01_one_to_many.py`

Use a publisher and its books.

```python
class Publisher:
    def __init__(self, name):
        self.name = name
        self.books = []

class Book:
    def __init__(self, title, publisher):
        self.title = title
        self.publisher = publisher
        publisher.books.append(self)
```

Create some objects:

```python
penguin = Publisher("Penguin")

book1 = Book("Python Basics", penguin)
book2 = Book("Learning APIs", penguin)

print(book1.publisher.name)
print([book.title for book in penguin.books])
```

### Talking Points

There are **two directions** to the relationship.

From Book:

```python
book1.publisher
```

From Publisher:

```python
penguin.books
```

Ask:

> "Which side has one object, and which side can contain many?"

Draw:

```text
Publisher
   |
   |---- Book
   |---- Book
   |---- Book
```

Emphasize that this is **one publisher to many books**.

---

## Example 2 - Medium: Many-to-Many

> Run it: `python demos/02_many_to_many.py`

Now introduce authors.

An author can write many books.

A book can have many authors.

```text
Author <-> Book
```

Ask students:

> "Where would we put `author_id`?"

Let them recognize that a single reference is no longer enough.

Introduce an association object:

```text
Author
   |
 Contract
   |
 Book
```

Now many Contract objects allow both sides to connect many times.

```python
class Contract:
    all = []

    def __init__(self, author, book):
        self.author = author
        self.book = book
        Contract.all.append(self)
```

Relationships can now be calculated.

```python
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
        return [
            contract.book
            for contract in self.contracts()
        ]
```

### Key Question

> Run it: `python demos/03_contract_metadata.py`

Ask:

> "Why isn't Contract just annoying extra code?"

Then add metadata:

```python
class Contract:
    all = []

    def __init__(self, author, book, royalty):
        self.author = author
        self.book = book
        self.royalty = royalty
        Contract.all.append(self)
```

Now the relationship itself contains information.

```text
Author -- Contract -- Book
           |
        royalty
```

This is a major reason association objects are useful.

---

## Example 3 - Complex: Relationships Become Application Behavior

> Run it: `python demos/04_model_vs_cli.py`

Suppose the CLI needs to show every book written by an author.

We should not recreate relationship logic inside the CLI.

Bad:

```python
def show_author_books(author):
    books = []

    for contract in Contract.all:
        if contract.author == author:
            books.append(contract.book)

    for book in books:
        print(book.title)
```

Better:

```python
def show_author_books(author):
    for book in author.books():
        print(book.title)
```

Ask:

> "Which version should know how authors and books are related?"

Answer:

**The model should know the relationship. The CLI should know how to interact with the user.**

That separation becomes increasingly important as applications grow.

---

# 0:30-0:45 - Real-World Application Walkthrough

## Turning the Model into an Application

Present the application structure:

```text
publishing_app/
|
|-- models.py
|-- cli.py
|-- services.py
`-- data/
    `-- books.json
```

Ask:

> "Why might this be easier to work with than one 500-line Python file?"

Connect directly to Module 6.

### models.py

Contains domain logic.

```python
class Author:
    ...

class Book:
    ...

class Contract:
    ...
```

### cli.py

Contains user interaction.

```python
from models import Author, Book, Contract
```

Menu:

```python
def menu():
    print("1. List authors")
    print("2. View author's books")
    print("3. Create contract")
    print("4. Exit")
```

Main loop:

```python
def main():
    while True:
        menu()

        choice = input("> ")

        if choice == "1":
            list_authors()

        elif choice == "2":
            show_author_books()

        elif choice == "3":
            create_contract()

        elif choice == "4":
            break

        else:
            print("Invalid option.")
```

Then:

```python
if __name__ == "__main__":
    main()
```

### Facilitator Talking Point

Explain the flow:

```text
USER
 |
CLI
 |
MODEL
 |
RELATED OBJECTS
```

The CLI should mostly be an orchestrator.

It asks:

1. What does the user want?
2. Which object should handle that operation?
3. How should the result be displayed?

---

# 0:45-1:05 - Guided Build

## Challenge: Implement "View an Author's Books"

Show students the desired behavior first.

```text
Publishing Manager

1. List authors
2. View author's books
3. Create contract
4. Exit

> 2

Choose an author:

1. Octavia Butler
2. Neil Gaiman
3. N. K. Jemisin

> 1

Books by Octavia Butler:

- Kindred
- Parable of the Sower
```

Ask the group:

> "What steps does our program need to perform?"

Guide students toward:

```text
Get authors
|
Display authors
|
Receive user choice
|
Find Author object
|
Ask Author for books
|
Display books
```

Build the function collaboratively.

```python
def show_author_books():
    authors = Author.all

    for index, author in enumerate(authors, start=1):
        print(f"{index}. {author.name}")

    choice = int(input("Choose an author: "))

    author = authors[choice - 1]

    print(f"\nBooks by {author.name}:")

    for book in author.books():
        print(f"- {book.title}")
```

Pause at:

```python
authors[choice - 1]
```

Ask:

> "Why are we subtracting one?"

This gives a quick opportunity to reinforce zero-based indexing.

Then ask:

> "What can go wrong here?"

Students should identify possibilities such as:

```text
User enters "hello"
User enters 0
User enters 27
Author has no books
```

Improve it:

```python
def show_author_books():
    authors = Author.all

    for index, author in enumerate(authors, start=1):
        print(f"{index}. {author.name}")

    try:
        choice = int(input("Choose an author: "))
        author = authors[choice - 1]

    except (ValueError, IndexError):
        print("Please choose a valid author.")
        return

    books = author.books()

    if not books:
        print("No books found.")
        return

    print(f"\nBooks by {author.name}:")

    for book in books:
        print(f"- {book.title}")
```

### Discussion

Ask:

> "Should validation live in the model or CLI?"

Use this to discuss **separation of concerns** rather than presenting one universal rule.

The model protects business/domain rules.

The CLI protects the user experience and translates user input into something the model understands.

---

# 1:05-1:17 - Extend the Application: External Services

Transition:

> "Our CLI works.
> Now imagine the product manager asks us to add an AI-generated publishing brief for a selected author."

Show the tempting approach:

```python
def generate_brief():
    # get user
    # find author
    # construct prompt
    # call API
    # parse API response
    # print output
```

Then ask:

> "What happens when three other features also need the same API?"

Introduce a reusable client.

```python
# services.py

class AIClient:
    def __init__(self, client):
        self.client = client

    def generate(self, prompt):
        response = self.client.generate(prompt)
        return response
```

The CLI can now use it:

```python
def generate_author_brief(author, ai_client):
    titles = [book.title for book in author.books()]

    prompt = f"""
    Create a short publishing brief.

    Author: {author.name}
    Books: {", ".join(titles)}
    """

    return ai_client.generate(prompt)
```

Show the architecture:

```text
                 +--------------+
                 | External API |
                 +------^-------+
                        |
                  services.py
                        ^
                        |
User --> cli.py --> models.py
```

### Key Talking Point

The external service doesn't need to understand the entire application.

The models don't need to understand how the API works.

The CLI coordinates them.

Connect this to professional software:

> **We isolate responsibilities so changing one part of an application doesn't force us to rewrite every other part.**

---

# 1:17-1:25 - Problem-Solving Challenge

Give students this scenario:

> We need to add a menu option called **"Create Contract."**
>
> The user should select an author, select a book, enter a royalty percentage, and create the relationship.

Display:

```text
1. Maya Angelou
2. James Baldwin
3. Toni Morrison

Choose author: 2

1. Book A
2. Book B
3. Book C

Choose book: 1

Royalty percentage: 12.5

Contract created!
```

Ask students to identify what belongs in each layer.

```text
CLI
Model
Service
```

Expected reasoning:

**CLI**

Handles:

```text
Display choices
Read input
Validate menu selections
Display success/error messages
```

**Contract model**

Handles:

```text
Author relationship
Book relationship
Royalty
Business validation
```

For example:

```python
class Contract:
    def __init__(self, author, book, royalty):
        if not 0 <= royalty <= 100:
            raise ValueError(
                "Royalty must be between 0 and 100."
            )

        self.author = author
        self.book = book
        self.royalty = royalty
```

Ask:

> "Why should the model validate royalty instead of trusting the CLI?"

Key answer:

Because tomorrow the object may be created somewhere other than the CLI.

For example:

```text
CLI
Web application
Automated script
API
Tests
```

Domain rules should therefore travel with the domain model.

---

# 1:25-1:30 - Wrap-Up / Exit Ticket

Do not end early.

Use the final five minutes to connect all three modules.

Draw:

```text
MODULE 5
Object Relationships
      |
How is our data connected?

MODULE 6
Application Configuration
      |
How is our code organized?

MODULE 7
CLI + External Services
      |
How does a user interact with our application,
and how does our application interact with
the outside world?
```

Ask students to answer three questions verbally or in chat:

**1. Relationships**

Why do we need an association object for many-to-many relationships?

**2. Application Structure**

Why would we separate `models.py`, `cli.py`, and `services.py`?

**3. CLI**

When a user selects an author from a menu, what ultimately connects that selection to their books?

Finish with the larger takeaway:

> "The important progression this week isn't memorizing three separate topics.
> You're learning how pieces of a real Python application work together.
> Objects represent the domain.
> Relationships connect those objects.
> Modules organize the code.
> The CLI gives users access to the objects, and service classes let your program communicate with systems outside your application."

### Lab Connection

Before students leave, explicitly connect the session to their assessments:

**Book Contracts Lab:**
Focus on correctly modeling and navigating many-to-many relationships.

**Pip/PyPI/Scripting Lab:**
Focus on application organization, dependencies, imports, and executable Python programs.

**Python CLI Tool Lab:**
Focus on translating user input into model operations while keeping the interface understandable.

**Shift Brief AI CLI Tool:**
Focus on combining the layers:

```text
CLI
+
Python objects
+
application organization
+
external service
+
reusable client class
```

The goal is for students to see these not as separate lessons, but as pieces of the same application-development workflow.
