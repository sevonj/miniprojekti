*** Settings ***
Library  ../AppLibrary.py
Resource    resource.robot
*** Variables ***

*** Test Cases ***

User Can Import Exported Data After Successful In-App Deletion
    Add Input  Add
    Add New Entry
    Add Input  Export
    Add Input    test-export-import.bib
    Add Input  Delete
    Add Input  All
    Add Input  y
    Add Input  Import
    Add Input    test-export-import.bib
    Add Input  List
    Add Input  Exit
    Run Application
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    Imported from
    Output Should Contain    Testaaja, Teppo

