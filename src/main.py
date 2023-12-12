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
    welcome,
    get_prompt,
    confirm_unsaved,
)

WELCOME_MSG = """
 M I N I P R O J E K T I 
    Citation Manager
  by Ryhmä4

Type HELP for help."""


def main(io):
    """The command loop"""

    app = App()
    app.create_bib()

    welcome()

    # App loop
    while True:
        command = io.input(get_prompt(app)).upper().strip()

        match command:
            case "EXIT":
                if confirm_unsaved(io, app):
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
            case "":
                pass
            case _:
                io.print(f"Unrecognized command: '{command}'")

    # Exit message.
    io.print("Have a nice day.")


if __name__ == "__main__":
    main(AppIO())
