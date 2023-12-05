*** Settings ***
Library  ../AppLibrary.py
Resource    resource.robot
*** Variables ***

*** Test Cases ***

User Can Load Saved Data After Successful In-App Deletion
    Add Input  Add
    Add New Entry
    Add Input  Save
    Add Input    test-export-load.bib
    Add Input  Delete
    Add Input  All
    Add Input  y
    Add Input  Load
    Add Input    test-export-load.bib
    Add Input  List
    Add Input  Exit
    Run Application
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    Loaded from
    Output Should Contain    Testaaja, Teppo

User Can Load from File Without Any Extension
    Add Input  Add
    Add New Entry
    Add Input  Save
    Add Input    test-export-Loadbbbbb
    Add Input  Delete
    Add Input  All
    Add Input  y
    Add Input  Load
    Add Input    test-export-Loadbbbbb
    Add Input  List
    Add Input  Exit
    Run Application
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    Loaded from
    Output Should Contain    Testaaja, Teppo


User Can Not Load From Non Existent File
    Add Input  Load
    Add Input    non-existent-test-export-Load.bib
    Add Input  List
    Add Input  Exit
    Run Application
    Output Should Contain    Loading file failed

