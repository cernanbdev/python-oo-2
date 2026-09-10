"""User interaction. This layer reads input, prints output, and delegates.

It knows how to talk to a person. It does not know how authors and books are
related, and it does not know that an AI provider exists.
"""

from publishing_app.models import Author
from publishing_app.seed import load_data


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
        print(f"{index}. {author.name}")


def show_author_books():
    # TODO (0:45 build)
    #
    #   Get authors -> display them -> read a choice -> find the Author object
    #   -> ask the Author for its books -> display them.
    #
    # Then ask the room: what can a user type that breaks this?
    print("Not built yet.")


def create_contract():
    # TODO (1:17 challenge)
    #
    #   Choose an author, choose a book, enter a royalty, create the contract.
    #   Decide out loud which layer owns each of those four steps.
    print("Not built yet.")


def generate_author_brief():
    # TODO (1:05 build)
    #
    #   Choose an author, build a prompt from that author's books, hand the
    #   prompt to the AI client, print the result. Where does each step live?
    print("Not built yet.")


def main():
    load_data()

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
            generate_author_brief()

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
