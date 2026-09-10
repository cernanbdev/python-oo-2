# Facilitator Runsheet

Keep this open on your **second screen**.
Share only the editor and terminal on the screen students see.

`AGENDA.md` is the teaching script.
This file is the operator's manual: what to type, when, and what to do when something goes sideways.

---

## Pre-flight (do this before students join)

```bash
cd python-oo-2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q                          # 33 passed
printf '1\n5\n' | python -m publishing_app.cli   # starter runs, prints the author list
```

Then reset your live-coding target so nothing from a rehearsal is left behind:

```bash
git status                         # should be clean
git checkout -- publishing_app     # if it is not
```

Set your terminal font large enough to read at the back of a Zoom grid.
Close the `solution/` directory in your editor's file tree so students do not see the answers in the sidebar.

---

## The two branches

The answers are not in the folder you are sharing.
They are on a second branch, checked out beside it.

| Branch | `publishing_app/` contains | Also has |
|---|---|---|
| `main` | The starter. Runs from minute one; the three build targets are `TODO` stubs. | `demos/` |
| `solution` | The finished application, matching this runsheet's end state. | `tests/` |

You teach from `main`.
`../publishing-solution` is the `solution` branch on disk (see pre-flight).

```bash
python -m publishing_app.cli                    # what you are building

cd ../publishing-solution
python -m publishing_app.cli                    # the finished version
pytest -q                                       # 33 passing tests
```

If you need to bail out mid-build, `cd ../publishing-solution` and keep teaching from the working app.
Do not switch branches in the shared folder while you have live-typed code in it.

---

## Where the repo differs from the agenda snippets

Say these out loud when you reach them.
Each one is a real teaching moment, not a discrepancy to hide.

**1. Imports.**
The agenda shows `from models import Author`.
The repo uses `from publishing_app.models import Author`, run with `python -m publishing_app.cli`.

The short version for students: the bare form only works when Python is already sitting inside that folder.
The package form works from anywhere, which is why it is what real projects use.
This is the Module 6 point, and it costs about ninety seconds.

**2. The menu has five options, not four.**
`4. Generate author brief` is added so the 1:05 service block has somewhere to land.
Exit is `5`.

**3. Seed data lives in `data/books.json`.**
`seed.py` reads it and builds the objects.
Nobody hard-codes a book list in `models.py`.

**4. Two seeded objects exist purely for demos.**

- **Ted Chiang** has no contracts, so option 2 shows the "no books" branch on a real author.
- **Exhalation** has no contract, so it is the obvious thing to sign at 1:17.

Signing Ted Chiang to Exhalation and then re-running option 2 is the cleanest payoff moment in the session.
Use it.

**5. `Good Omens` has two authors** (Gaiman and Pratchett).
It is the seeded proof that many-to-many is not hypothetical.

---

## Minute by minute

### 0:00-0:15 - Q&A

Nothing to run.
Keep a visible running list of what comes up; you will call back to it.

Diagnostic questions are in `AGENDA.md`.

### 0:15-0:30 - Concept review

Run the demos in order, in the terminal, one at a time:

```bash
python demos/01_one_to_many.py
python demos/02_many_to_many.py
python demos/03_contract_metadata.py
python demos/04_model_vs_cli.py
```

Each script is short enough to show the whole file on screen alongside its output.

Beats worth hitting:

- Demo 01: two directions, one relationship.
- Demo 02: ask "where does `author_id` go?" **before** you show `Contract`. Let the room get stuck.
- Demo 03: royalty is a fact about the agreement, not about the author and not about the book. This is the answer to "isn't Contract just extra code?"
- Demo 04: same output, two designs. Ask which one should know the relationship.

### 0:30-0:45 - Application walkthrough

Open the starter package in this order: `models.py`, then `seed.py`, then `cli.py`, then `services.py`.

Then run it:

```bash
python -m publishing_app.cli
```

Pick option 1, then option 2.
Option 2 says `Not built yet.`
That is the setup for the next block.

Key line to deliver while `cli.py` is on screen:
the CLI file contains no loops over `Contract.all`, and it never will.

### 0:45-1:05 - Build "View an Author's Books"

**Type this into `publishing_app/cli.py`, replacing the `show_author_books` stub.**

Start with the naive version from the agenda, run it, break it on purpose (type `hello`, then `0`, then `27`), and only then harden it.

Final state:

```python
def show_author_books():
    authors = Author.all

    for index, author in enumerate(authors, start=1):
        print(f"{index}. {author.name}")

    try:
        choice = int(input("\nChoose an author: "))
        author = authors[choice - 1]

    except (ValueError, IndexError):
        print("Please choose a valid author.")
        return

    books = author.books()

    if not books:
        print(f"\n{author.name} has no books under contract yet.")
        return

    print(f"\nBooks by {author.name}:\n")

    for book in books:
        print(f"- {book.title}")
```

Two things to pause on:

- `authors[choice - 1]` - menus start at 1, lists start at 0.
- `choice = 0` gives you `authors[-1]`, which is a *silent* wrong answer rather than a crash. It is the best bug in the session. Show it.

Then demo option 2 with **Ted Chiang (8)** to hit the empty branch.

### 1:05-1:17 - External services

Open `publishing_app/services.py`.
Both backends are already written; point out that `EchoBackend` means the app works with no key and no network, which is why this demo cannot fail.

**Type this, replacing the `AIClient` TODO:**

```python
class AIClient:
    def __init__(self, backend):
        self.backend = backend

    def generate(self, prompt):
        try:
            return self.backend.generate(prompt)
        except AIServiceError:
            raise
        except Exception as error:
            raise AIServiceError(f"The AI service failed: {error}") from error
```

**Then finish `build_ai_client`:**

```python
def build_ai_client():
    load_dotenv()

    if os.getenv("ANTHROPIC_API_KEY"):
        return AIClient(AnthropicBackend())

    return AIClient(EchoBackend())
```

**Then wire the CLI.** In `publishing_app/cli.py`:

```python
from publishing_app.services import AIServiceError, build_ai_client, build_author_brief_prompt


def generate_author_brief(ai_client):
    authors = Author.all

    for index, author in enumerate(authors, start=1):
        print(f"{index}. {author.name}")

    try:
        author = authors[int(input("\nChoose an author: ")) - 1]
    except (ValueError, IndexError):
        print("Please choose a valid author.")
        return

    print("\nGenerating...\n")

    try:
        print(ai_client.generate(build_author_brief_prompt(author)))
    except AIServiceError as error:
        print(f"Could not generate a brief. {error}")
```

And in `main`, build the client once and pass it in:

```python
def main():
    load_data()
    ai_client = build_ai_client()
    ...
        elif choice == "4":
            generate_author_brief(ai_client)
```

The point to land: `AIClient` is not a pointless pass-through.
It exists so that every way the outside world can fail arrives at the CLI as one error type, and the CLI needs exactly one `except`.
Swapping providers is a change in one file.

If you have a key in `.env`, run it live for real output.
If not, the offline brief prints and the lesson is identical.

### 1:17-1:25 - Create Contract challenge

Ask the layering question first.
Let them answer before you type.

**In `publishing_app/models.py`, add the rule to `Contract.__init__`:**

```python
        if not 0 <= royalty <= 100:
            raise ValueError("Royalty must be between 0 and 100.")
```

**And add `sign` to `Author`:**

```python
    def sign(self, book, royalty):
        return Contract(self, book, royalty)
```

**In `publishing_app/cli.py`,** note that you now need to number a list twice.
Extract the helper live - this is the natural moment for it:

```python
def choose_from(items, prompt, label):
    for index, item in enumerate(items, start=1):
        print(f"{index}. {label(item)}")

    try:
        choice = int(input(prompt))
    except ValueError:
        print("Please enter a number.")
        return None

    if choice < 1 or choice > len(items):
        print("That is not one of the options.")
        return None

    return items[choice - 1]


def create_contract():
    author = choose_from(Author.all, "\nChoose author: ", lambda a: a.name)

    if author is None:
        return

    print()
    book = choose_from(Book.all, "\nChoose book: ", lambda b: b.title)

    if book is None:
        return

    try:
        royalty = float(input("\nRoyalty percentage: "))
    except ValueError:
        print("Royalty must be a number.")
        return

    try:
        contract = author.sign(book, royalty)
    except (TypeError, ValueError) as error:
        print(error)
        return

    print(f"\nContract created: {contract.author.name} / {contract.book.title} at {contract.royalty}%")
```

Remember to add `Book` to the import at the top of `cli.py`.

**Then cash the helper in.**
`show_author_books` and `generate_author_brief` both still have their own numbering loop.
Delete both loops and call `choose_from` instead:

```python
def show_author_books():
    author = choose_from(Author.all, "\nChoose an author: ", lambda a: a.name)

    if author is None:
        return
    ...
```

```python
def generate_author_brief(ai_client):
    author = choose_from(Author.all, "\nChoose an author: ", lambda a: a.name)

    if author is None:
        return
    ...
```

That is about thirty seconds of deleting, and it is the strongest argument in the session for extracting a function.
`choose_from` checks the range explicitly, so it does not have the `choice = 0` bug you demonstrated at 0:45.
You did not just remove three copies of a loop.
You removed three copies of a bug, and you will never write the fourth.

**The demo:** sign **Ted Chiang (8)** to **Exhalation (11)** at **12.5**, then immediately pick option 2 and choose Ted Chiang.
The book he did not have a minute ago is now there.
Nothing in `show_author_books` changed.

Then try a royalty of **150** and let the model reject it.
Ask: which file printed that message, and which file decided it was wrong?

If you have time, run the tests on screen from the solution checkout:

```bash
(cd ../publishing-solution && pytest -q)
```

33 tests, no network, no API key, no typing into a menu.
That is what the layering bought you.

Run them from there rather than against your live-typed code.
The assertions match the runsheet exactly, and a red suite caused by a stray wording change is not the lesson you want on screen at 1:24.

### 1:25-1:30 - Wrap-up

Do not end early.
The three exit-ticket questions are in `AGENDA.md`.

The third one - "what connects that selection to their books?" - should now have a concrete answer they watched you build: `Contract.all`.

---

## If you fall behind

Cut in this order:

1. The `choose_from` extraction at 1:17. Write `create_contract` with a copy of the numbering loop and name the duplication out loud instead.
2. The naive-then-harden pass at 0:45. Type the hardened `show_author_books` directly and discuss the failure modes without demonstrating each one.
3. Demo 01. It is the one concept most students already have.

Never cut the 1:17 layering discussion.
It is the point of the session.

---

## Stretch questions if you are ahead

- Should `Contract` reject a duplicate author/book pair? Which layer catches it?
- `Publisher.authors()` in `models.py` walks books to reach authors. Trace the hops out loud.
- What breaks if two authors share a name? What is `Author.all` really keyed on?
- Why does `seed.py` exist instead of a `load()` method on each model?
- The tests never touch the network. Find the seam in `services.py` that makes that possible.

---

## Emergency commands

```bash
git checkout -- publishing_app                       # undo everything you typed live
git diff                                             # show the room exactly what you just wrote

cd ../publishing-solution && python -m publishing_app.cli   # run the finished app
cd ../publishing-solution && pytest -q                      # 33 passing tests
```

To see the finished version of one file without leaving your editor:

```bash
git show solution:publishing_app/cli.py
```
