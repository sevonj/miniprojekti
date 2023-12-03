*** Settings ***
Library  ../AppLibrary.py
Resource    resource.robot
*** Variables ***

*** Test Cases ***
User Can Export Added Entry
    Add Input  Add
    Add New Entry
    Add Input  EXPORT
    Add Input  test.bib
    Add Input  exit
    Run Application
    Skip Output
    Skip Output
    Output Should Contain    Exported to


User Cannot Export To Path Containing Forbidden Chars
    Add Input  Add
    Add New Entry
    Add Input  EXPORT
    Add Input  /
    Add Input  exit
    Run Application
    Skip Output
    Skip Output
    Output Should Contain    Try another file name

User Cannot Export To Path Containing Non-Existent Dir Structure
    Add Input  Add
    Add New Entry
    Add Input  EXPORT
    Add Input  folder/folder/folder/asdf.bib
    Add Input  exit
    Run Application
    Skip Output
    Skip Output
    Output Should Contain    Try another file name