*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot


*** Test Cases ***
List Command Can Be Executed
    Add Input    add
    Add New Entry
    Add Input    list
    Add Input    exit
    Add Input    y
    Run Application
    Output Should Contain    Enter article citation details
    Output Should Contain    Entry successfully added to the database
    Skip Output
    Output Should Contain    Testaaja, Teppo

List Command Return Infomessage If No Entries
    Add Input    list
    Add Input    exit
    Run Application
    Output Should Contain    No entries found
