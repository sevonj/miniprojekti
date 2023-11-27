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

Add Command Can Be Executed
    Add Input  add
    Input New Entry    Teppo Testaaja    Test Article    Journal of Articles    2023    N/A    N/A    N/A
    Add Input  exit
    Run Application
    Output Should Contain  Enter article citation details

New Entry Can Be Added
    Add Input  add
    Input New Entry    Teppo Testaaja    Test Article    Journal of Articles    2023    N/A    N/A    N/A
    Add Input  exit
    Run Application
    Output Should Contain  Enter article citation details
    Output Should Contain  Entry successfully saved to the database

List Command Return Infomessage If No Entries
    Add Input  list
    Add Input  exit
    Run Application
    Output Should Contain  No entries found

*** Keywords ***
Input New Entry
    [Arguments]    ${author}    ${title}    ${journal}    ${year}    ${volume}    ${number}    ${pages}
    Add Input    ${author}
    Add Input    ${title}
    Add Input    ${journal}
    Add Input    ${year}
    Add Input    ${volume}
    Add Input    ${number}
    Add Input    ${pages}
