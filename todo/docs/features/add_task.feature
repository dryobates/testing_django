Feature: Add task

    As logged user
    In order to not forget what I need to do
    I want to add task to todo list

Scenario: Adding task

    Given user "test1" exists
    When I visit "/" as logged user "test1"
    And I enter "buy bread" in field "title"
    And I enter "5" in field "priority"
    And I press button "submit"
    Then I see task "buy bread" on tasks list
