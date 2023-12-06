*** Settings ***
Library  ../AppLibrary.py
Resource    resource.robot
*** Variables ***

*** Test Cases ***
User Can Save Added Entry
    Add Input  Add
    Add New Entry
    Add Input  Save
    Add Input  test.bib
    Add Input  exit
    Run Application
    Skip Output    2
    Output Should Contain    Saved to


User Cannot Save To Path Containing Forbidden Chars
    Add Input  Add
    Add New Entry
    Add Input  Save
    Add Input  /
    Add Input  exit
    Run Application
    Skip Output    2
    Output Should Contain    Try another file name

User Cannot Save To Path Containing Non-Existent Dir Structure
    Add Input  Add
    Add New Entry
    Add Input  Save
    Add Input  folder/folder/folder/asdf.bib
    Add Input  exit
    Run Application
    Skip Output    2
    Output Should Contain    Try another file name