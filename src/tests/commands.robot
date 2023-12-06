*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot


*** Test Cases ***
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
    Run Application
    Output Should Contain    Enter article citation details

Search Command Can Be Executed
    Add Input    add
    Add New Entry
    Add Input    search
    Add Input    art
    Add Input    exit
    Run Application
    Skip Output    2
    Output Should Contain    Testaaja, Teppo

New Entry Can Be Added
    Add Input    add
    Add New Entry
    Add Input    exit
    Run Application
    Output Should Contain    Enter article citation details
    Output Should Contain    Entry successfully added to the database
