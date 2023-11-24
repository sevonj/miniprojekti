*** Settings ***
Library  ../AppLibrary.py
*** Variables ***

*** Test Cases ***
Test Exit
    Add Input  exit
    Run Application
    Output Should Contain  Enter command (ADD/LIST/EXIT): 
    Output Should Contain  Have a nice day. 
    

*** Keywords ***
