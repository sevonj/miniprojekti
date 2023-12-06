*** Settings ***
Library  ../AppLibrary.py

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
    [Arguments]    ${title}="Test Article"
    Input New Entry Details    Teppo Testaaja    ${title}    Journal of Articles    2023    N/A    N/A    N/A
    
