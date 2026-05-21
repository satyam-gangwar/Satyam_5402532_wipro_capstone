Feature: 99acres Login

  Scenario: Login with valid mobile number using OTP
    Given user launches the 99acres application
    When user opens the login popup
    And user enters valid mobile number
    And user waits for OTP verification
    Then user should be logged in successfully