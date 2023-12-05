*** Settings ***
Library  ../AppLibrary.py
Resource    resource.robot
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
    Add New Entry
    Add Input  exit
    Run Application
    Output Should Contain  Enter article citation details

List Command Can Be Executed
    Add Input  add
    Add New Entry
    Add Input  list
    Add Input  exit
    Run Application
    Output Should Contain  Enter article citation details
    Output Should Contain  Entry successfully saved to the database
    Output Should Contain  Testaaja, Teppo

Search Command Can Be Executed
    Add Input  add
    Add New Entry
    Add Input  search
    Add Input  art
    Add Input  exit
    Run Application
    Skip Output
    Skip Output
    Output Should Contain    Testaaja, Teppo
    
New Entry Can Be Added
    Add Input  add
    Add New Entry
    Add Input  exit
    Run Application
    Output Should Contain  Enter article citation details
    Output Should Contain  Entry successfully saved to the database

List Command Return Infomessage If No Entries
    Add Input  list
    Add Input  exit
    Run Application
    Output Should Contain  No entries found

Delete All Clears BiblioGraphy
    Add Input    Add
    Add New Entry
    Add Input    Add
    Add New Entry_2
    Add Input    Add
    Add New Entry_3
    Add Input    delete
    Add Input    All
    Add Input    y
    Add Input    list
    Add Input    exit
    Run Application
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    No entries found

User Can Delete One Entry
    Add Input    Add
    Add New Entry
    Add Input    Add
    Add New Entry_2
    Add Input    Add
    Add New Entry_3
    Add Input    delete
    Add Input    1
    Add Input    y
    Add Input    list
    Add Input    exit
    Run Application
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    Testaaja, Teppo

Search Doi Command Can Be Executed
    Add Input  doi
    Add Input  ${EMPTY}
    Add Input  exit
    Run Application
    Output Should Contain    DOI is missing, search cancelled

User Gets Doi Search Result As A List
    Add Input  doi
    Add Input  10.1145/2783446.2783605
    Add Input  n
    Add Input  exit
    Run Application
    Output Should Contain    Framing the community data system interface

User Can Add Doi Search Result To BiblioGraphy
    Add Input  doi
    Add Input  10.1145/2783446.2783605
    Add Input  y
    Add Input  list
    Add Input  exit
    Run Application
    Output Should Contain    Framing the community data system interface
    Output Should Contain    Entry successfully saved to the database
    Output Should Contain    Framing the community data system interface

*** Keywords ***
Input New Entry Details
    [Arguments]    ${author}    ${title}    ${journal}    ${year}    ${volume}    ${number}    ${pages}
    Add Input    ${author}
    Add Input    ${title}
    Add Input    ${journal}
    Add Input    ${year}
    Add Input    ${volume}
    Add Input    ${number}
    Add Input    ${pages}

Add New Entry
    Input New Entry Details    Teppo Testaaja    Test Article    Journal of Articles    2023    N/A    N/A    N/A

Add New Entry_2
    Input New Entry Details    Teppo Testaaja    Test Article_2    Journal of Articles    2023    N/A    N/A    N/A
    
Add New Entry_3
    Input New Entry Details    Teppo Testaaja    Test Article_3    Journal of Articles    2023    N/A    N/A    N/A

Add New Entry_4
    Input New Entry Details    Teppo Testaaja    Test Article_4    Journal of Articles    2023    N/A    N/A    N/A

Add New Entry_5
    Input New Entry Details    Teppo Testaaja    Test Article_5    Journal of Articles    2023    N/A    N/A    N/A
