Feature: 99acres Commercial Negative Search

  @commercial @negative
  Scenario Outline: Search commercial property with invalid location
    Given User launches 99acres application
    When User opens Commercial tab
    And User searches commercial property for location "<invalid_location>"
    Then Invalid commercial search should be handled

    Examples:
      | invalid_location |
      | @@@@@@@@@@    |


  @commercial @negative_empty_search
  Scenario: Search commercial property without entering location

    Given User launches 99acres application

    When User opens Commercial tab

    And User clicks Commercial Search button

    Then Invalid commercial search should be handled