"""
main.py

This module manages the UI and App service

"""
from app_io import AppIO
from app import App
from ui import (
    add_entry,
    del_entries,
    get_entries,
    load_entries,
    print_help,
    save_entries,
    search_doi,
    search_entries,
    edit_entry,
)


def main(io):
    """The command loop"""

    app = App()
    app.create_bib()

    # App loop
    while True:
        command = io.input("Enter command (type HELP for help):\n> ").upper().strip()

        match command:
            case "EXIT":
                break

            case "HELP":
                print_help(io)

            case "ADD":
                add_entry(io, app)

            case "DOI":
                search_doi(io, app)

            case "DELETE":
                del_entries(io, app)

            case "LIST":
                get_entries(io, app)

            case "SEARCH":
                search_entries(io, app)

            case "SAVE":
                save_entries(io, app)

            case "LOAD":
                load_entries(io, app)

            case "EDIT":
                edit_entry(io, app)

            case _:
                io.print(f"Unrecognized command: '{command}'")

    # Exit message.
    io.print("Have a nice day.")


if __name__ == "__main__":
    main(AppIO())
