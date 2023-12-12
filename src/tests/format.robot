*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot


*** Test Cases ***
Long List Of Authors Is Formatted When Listed
    Add Input    add
    Add New Entry With Over 3 Authors
    Add Input    list
    Add Input    exit
    Add Input    y
    Run Application
    Output Should Contain    Enter article citation details
    Output Should Contain    Entry successfully added to the database
    Skip Output
    Output Should Contain    Testaaja, Teppo et al.

Three Authors Are Formatted When Listed
    Add Input    add
    Add New Entry With Three Authors
    Add Input    list
    Add Input    exit
    Add Input    y
    Run Application
    Output Should Contain    Enter article citation details
    Output Should Contain    Entry successfully added to the database
    Skip Output
    Output Should Contain    Testaaja, Teppo and Testaaja, Seppo and Tester, Max
  

Too Long Title Name Is Trimmed When Listed
    Add Input    add
    Add New Entry With Long Title
    Add Input    list
    Add Input    exit
    Add Input    y
    Run Application
    Output Should Contain    Enter article citation details
    Output Should Contain    Entry successfully added to the database
    Skip Output
    Output Should Contain    Test Article 4, which is very much too ...
  


*** Keywords ***
Add New Entry With Three Authors
    [Arguments]    ${title}="Test Article 2"
    Input New Entry Details    Teppo Testaaja and Seppo Testaaja and Max Tester  ${title}    Journal of Articles    2023    N/A    N/A    N/A

Add New Entry With Over 3 Authors
    [Arguments]    ${title}="Test Article 3"
    Input New Entry Details    Teppo Testaaja and Seppo Testaaja and Max Tester and Extra Tester   ${title}    Journal of Articles    2023    N/A    N/A    N/A

Add New Entry With Long Title
    [Arguments]    ${title}="Test Article 4, which is very much too long and should be trimmed"
    Input New Entry Details    Teppo Testaaja  ${title}    Journal of Articles    2023    N/A    N/A    N/A

