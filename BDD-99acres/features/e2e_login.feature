Feature: 99acres Login Functionality

  Background:
    Given User launches 99acres application

  @login @smoke
  Scenario: Open 99acres login popup
    When User clicks on Login button
    Then Login mobile number field should be displayed

  @login@mobile_number
  Scenario: Enter valid mobile number and continue to OTP screen
    When User clicks on Login button
    And User enters valid mobile number from test data
    And User clicks Continue button
    Then OTP screen should be displayed

  @login @manual_otp
  Scenario: Complete login with manually entered OTP
    When User submits valid mobile number for OTP
    And User enters OTP manually
    Then Login flow should continue after manual OTP entry

     @commercial @smoke
  Scenario: Search commercial property by location
    When User opens Commercial tab
    And User enters commercial property location "Hyderabad"
    And User clicks Commercial Search button
    Then User should be redirected to commercial results page

    @commercial @property_navigation
  Scenario: Navigate to any commercial property from results page
    Given User launches 99acres application
    When User opens Commercial tab
    And User enters commercial property location "Noida"
    And User clicks Commercial Search button
    Then User should be redirected to commercial results page
    When User clicks any commercial property from results
    Then Commercial property detail page should be opened