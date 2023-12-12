*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot


*** Test Cases ***
Normal Addition Works
    Add Input    add
    Add New Entry
    Add Input    list
    Add Input    exit
    Run Application
    Output Should Contain    Enter article citation details
    Output Should Contain    Entry successfully added to the database
    Output Should Contain    Testaaja, Teppo

User Can Edit Added Entry
    Add Input    add
    Add New Entry
    
