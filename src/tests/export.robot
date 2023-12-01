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
