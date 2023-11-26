*** Settings ***
Library  ../AppLibrary.py
*** Variables ***

*** Test Cases ***
Exit The App
    Add Input  exit
    Run Application
    Output Should Contain  Have a nice day. 

Help Command Can Be Executed
    Add Input  help
    Add Input  exit
    Run Application
    Output Should Contain  Available commands    

*** Keywords ***
