*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot


*** Test Cases ***
User Gets Feedback When Invoking Unrecognized Command
    Add Input    ASDF
    Add Input    exit
    Run Application
    Output Should Contain    Unrecognized command

Exit The App
    Add Input    exit
    Run Application
    Output Should Contain    Have a nice day.

Help Command Can Be Executed
    Add Input    help
    Add Input    exit
    Run Application
    Output Should Contain    Available commands

Add Command Can Be Executed
    Add Input    add
    Add New Entry
    Add Input    exit
    Add Input    y
    Run Application
    Output Should Contain    Enter article citation details

New Entry Can Be Added
    Add Input    add
    Add New Entry
    Add Input    exit
    Add Input    y
    Run Application
    Output Should Contain    Enter article citation details
    Output Should Contain    Entry successfully added to the database
