Feature: 99acres Commercial Module

  Background:
    Given User launches 99acres application

@commercial @smoke
Scenario: Search commercial property by location
  When User opens Commercial tab
And User enters commercial property location "Mumbai"
And User clicks Commercial Search button
Then User should be redirected to commercial results page

 # @commercial
  #Scenario Outline: Search shop commercial property
  #  When User opens Commercial tab
   # And User selects commercial property type "<property_type>"
    #And User searches commercial property for location "<location>"
    #Then Commercial results should be loaded

    #Examples:
     # | location | property_type |
      #| Noida    | Shop          |
      #| Delhi    | Shop          |

  #@commercial @view_number
  #Scenario: Verify View Number button opens login popup
  #  When User opens commercial city page for "Noida"
   # And User scrolls to View Number button
    #And User clicks View Number button
    #Then Login popup should be displayed on commercial page

  #@commercial @negative
  #Scenario: Search invalid commercial location
   # When User opens Commercial tab
   # And User searches commercial property for location "xyz123invalid"
    #Then Invalid commercial search should be handled

  #@commercial @negative
  #Scenario Outline: Open invalid commercial URL
   # When User opens invalid commercial URL "<invalid_url>"
   # Then Invalid commercial search should be handled

    #Examples:
     # | invalid_url |
      #| https://www.99acres.com/search/property/buy/commercial-property-in-@@@@ |
      #| https://www.99acres.com/search/property/buy/commercial-property-in-invalidcity123 |
