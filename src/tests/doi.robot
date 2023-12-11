*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot


*** Test Cases ***
Search Doi Command Can Be Executed
    Add Input    doi
    Add Input    ${EMPTY}
    Add Input    exit
    Run Application
    Output Should Contain    DOI is missing, search cancelled

User Gets Doi Search Result As A List
    Add Input    doi
    Add Input    10.1145/2783446.2783605
    Add Input    n
    Add Input    exit
    Run Application
    Output Should Contain    Framing the community data system interf...

User Can Add Doi Search Result To BiblioGraphy
    Add Input    doi
    Add Input    10.1145/2783446.2783605
    Add Input    y
    Add Input    list
    Add Input    exit
    Run Application
    Output Should Contain    Framing the community data system interf...
    Output Should Contain    Entry successfully saved to the database
    Skip Output
    Output Should Contain    Framing the community data system interf...

User Gets Infomessage If Doi Search Is Unsuccessful
    Add Input    doi
    Add Input    10.1215/0961754x-7299546
    Add Input    exit
    Run Application
    Output Should Contain    Invalid name format encountered

