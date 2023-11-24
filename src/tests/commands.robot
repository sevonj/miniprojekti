*** Settings ***
Library  ../AppLibrary.py
*** Variables ***

*** Test Cases ***
Exit The App
    Add Input  exit
    Run Application
    Output Should Contain  Have a nice day. 
    

*** Keywords ***
