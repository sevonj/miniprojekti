*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot


*** Test Cases ***
User Can Delete All Entries
    Add Input    Add
    Add New Entry
    Add Input    Add
    Add New Entry    Test Article 2
    Add Input    Add
    Add New Entry    Test Article 3
    Add Input    delete
    Add Input    All
    Add Input    y
    Add Input    list
    Add Input    exit
    Run Application
    Skip Output    7
    Output Should Contain    No entries found

User Can Delete Select Entries
    Add Input    Add
    Add New Entry
    Add Input    Add
    Add New Entry    Test Article 2
    Add Input    Add
    Add New Entry    Test Article 3
    Add Input    delete
    Add Input    1
    Add Input    y
    Add Input    list
    Add Input    exit
    Run Application
    Skip Output    7
    Output Should Contain    Testaaja, Teppo
