*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot

*** Test Cases ***
Entry Will Get A Citekey Based On First Author And Year
    Add Input    add
    Input New Entry Details    Mikko Mäkinen and Susanna Lahti    Our first Article    Kanditutkielmat    2023    N/A    N/A    N/A
    Add Input    list
    Add Input    exit
    Run Application
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    Mäkinen2023

Entry With Same Author And Year Will Get A Citekey Based On First Author, Year And Letter
    Add Input    add
    Input New Entry Details    Mikko Mäkinen and Susanna Lahti    Our first Article    Kanditutkielmat    2023    N/A    N/A    N/A
    Add Input    add
    Input New Entry Details    Mikko Mäkinen and Susanna Lahti    Our second Article    Kanditutkielmat    2023    N/A    N/A    N/A
    Add Input   list
    Add Input    exit
    Run Application
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Skip Output
    Output Should Contain    Mäkinen2023a


