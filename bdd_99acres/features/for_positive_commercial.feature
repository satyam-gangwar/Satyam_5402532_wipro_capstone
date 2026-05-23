Feature: 99acres Commercial Module

  Background:
    Given User launches 99acres application

  @commercial @smoke
  Scenario: Search commercial property by location
    When User opens Commercial tab
    And User enters commercial property location "Mumbai"
    And User clicks Commercial Search button
    Then User should be redirected to commercial results page


  @commercial @noida_filter
  Scenario: Search Noida commercial property and apply filters
    Given User launches 99acres application
    When User opens Commercial tab
    And User enters commercial property location "Noida"
    And User selects commercial location suggestion
    And User clicks Commercial Search button
    Then User should be redirected to commercial results page
    And Commercial results should contain location "Noida"
    When User applies Noida commercial filters
    Then Commercial results should be loaded




  @commercial @property_navigation
  Scenario: Navigate to any commercial property from results page
    Given User launches 99acres application
    When User opens Commercial tab
    And User enters commercial property location "Noida"
    And User clicks Commercial Search button
    Then User should be redirected to commercial results page
    When User clicks any commercial property from results
    Then Commercial property detail page should be opened



  @commercial @fixed_property
  Scenario: Open fixed commercial property from Noida results page
    Given User launches 99acres application
    When User opens Commercial tab
    And User enters commercial property location "Noida"
    And User clicks Commercial Search button
    Then User should be redirected to commercial results page
    When User clicks M3M commercial property
    Then Commercial property detail page should be opened

