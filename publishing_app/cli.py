"""User interaction. This layer reads input, prints output, and delegates.

It knows how to talk to a person. It does not know how authors and books are
related, and it does not know that an AI provider exists.
"""

from publishing_app.models import Author, Book
from publishing_app.seed import load_data
from publishing_app.services import AIServiceError, build_ai_client, build_author_brief_prompt


def menu():
    print("\nPublishing Manager\n")
    print("1. List authors")
    print("2. View author's books")
    print("3. Create contract")
    print("4. Generate author brief")
    print("5. Exit")
    print()


def list_authors():
    for index, author in enumerate(Author.all, start=1):
        count = len(author.books())
        label = "book" if count == 1 else "books"
        print(f"{index}. {author.name} ({count} {label})")


def choose_from(items, prompt, label):
    """Print a numbered list, read one choice, return the object or None.

    Turning "3" into an object is presentation work, so it belongs to the CLI.
    """
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

    # Menus start at 1, Python lists start at 0.
    return items[choice - 1]


def show_author_books():
    author = choose_from(Author.all, "\nChoose an author: ", lambda a: a.name)

    if author is None:
        return

    books = author.books()

    if not books:
        print(f"\n{author.name} has no books under contract yet.")
        return

    print(f"\nBooks by {author.name}:\n")

    for book in books:
        print(f"- {book.title}")


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
        # The model owns the rule. The CLI just reports the verdict.
        contract = author.sign(book, royalty)
    except (TypeError, ValueError) as error:
        print(error)
        return

    print(f"\nContract created: {contract.author.name} / {contract.book.title} at {contract.royalty}%")


def generate_author_brief(ai_client):
    author = choose_from(Author.all, "\nChoose an author: ", lambda a: a.name)

    if author is None:
        return

    prompt = build_author_brief_prompt(author)

    print("\nGenerating...\n")

    try:
        print(ai_client.generate(prompt))
    except AIServiceError as error:
        print(f"Could not generate a brief. {error}")


def main():
    load_data()
    ai_client = build_ai_client()

    while True:
        menu()

        choice = input("> ").strip()

        if choice == "1":
            list_authors()

        elif choice == "2":
            show_author_books()

        elif choice == "3":
            create_contract()

        elif choice == "4":
            generate_author_brief(ai_client)

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
