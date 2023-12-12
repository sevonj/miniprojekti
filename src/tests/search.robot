*** Settings ***
Library     ../AppLibrary.py
Resource    resource.robot


*** Test Cases ***
Search Command Can Be Executed
    Add Input    add
    Add New Entry
    Add Input    search
    Add Input    art
    Add Input    exit
    Add Input    y
    Run Application
    Skip Output    2
    Output Should Contain    Testaaja, Teppo

Search Command Returns correct row
    Add Input    add
    Add New Entry    AAAAAAAA
    Add Input    add
    Add New Entry    BBBBBBBB
    Add Input    add
    Add New Entry    CCCCCCCC
    Add Input    search
    Add Input    B
    Add Input    exit
    Add Input    y
    Run Application
    Skip Output    6
    Output Should Contain    BBBBBBBB
