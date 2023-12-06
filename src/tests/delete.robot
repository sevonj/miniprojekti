*** Settings ***
Library  ../AppLibrary.py
Resource    resource.robot
*** Variables ***

*** Test Cases ***

Delete All Clears BiblioGraphy
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
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    No entries found

User Can Delete One Entry
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
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    Testaaja, Teppo
