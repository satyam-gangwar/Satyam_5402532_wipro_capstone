import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.commercial_page import CommercialPage
from utilities.waits import WaitUtils


@allure.feature("Commercial Module")
class TestCommercial:

    @pytest.mark.commercial
    def test_commercial_flow(self, base_url, test_data):

        location = test_data["property_search"]["commercial_location"]

        home = HomePage(self.driver)

        # OPEN SITE
        home.open(base_url)
        home.wait_for_page_load()

        # OPEN COMMERCIAL TAB
        commercial = home.open_commercial_tab()

        # SEARCH
        commercial.search_commercial_property(location)

        # FILTER
        commercial.apply_basic_filters()

        # VALIDATE
        assert commercial.is_results_loaded()
        assert commercial.results_contain_location(location)





    @pytest.mark.commercial
    @pytest.mark.parametrize(
        "location",
        [

            ("Mumbai"),
            ("Delhi"),

        ]
    )
    def test_commercial_flow(self, base_url, location):
        home = HomePage(self.driver)

        # OPEN SITE
        home.open(base_url)
        home.wait_for_page_load()

        # OPEN COMMERCIAL TAB
        commercial = home.open_commercial_tab()

        # SEARCH
        commercial.search_commercial_property(location)

        # FILTER
        commercial.apply_basic_filters()

        # VALIDATE
        assert commercial.is_results_loaded()

        assert commercial.results_contain_location(location)

    @pytest.mark.commercial
    @pytest.mark.parametrize(
        "location, property_type",
        [
            ("Noida", "Shop")
        ]
    )
    def test_search_shop_showroom(self, base_url, location, property_type):
        home = HomePage(self.driver)

        home.open(base_url)
        home.wait_for_page_load()
        WaitUtils.slow_execution(self.driver, 2)

        commercial = home.open_commercial_tab()
        WaitUtils.slow_execution(self.driver, 2)

        commercial.select_property_type(property_type)
        WaitUtils.slow_execution(self.driver, 2)

        commercial.search_commercial_property(location)
        WaitUtils.slow_execution(self.driver, 3)

        assert commercial.is_results_loaded()

        print(f"{property_type} search successful in {location}")

        # Wait before closing browser
        WaitUtils.slow_execution(self.driver, 5)










    @pytest.mark.parametrize(
            "city",
            [
                "Noida"
            ]
    )
    def test_view_number_button(self, driver, city):
        # Open commercial property page
        driver.get(
            f"https://www.99acres.com/search/property/buy/commercial-property-in-{city.lower()}?keyword={city}"
        )

        driver.maximize_window()

        # Wait for page load
        WaitUtils.wait_for_page_load(driver)

        # Slow execution
        WaitUtils.slow_execution(driver, 2)

        # Wait for page content
        WaitUtils.wait_for_presence(
            driver,
            (
                By.XPATH,
                f"//*[contains(.,'{city}')]"
            )
        )

        # Scroll down slowly
        driver.execute_script(
            "window.scrollBy(0, 800);"
        )

        WaitUtils.slow_execution(driver, 2)

        # Contact / View Number button locator
        contact_locator = (
            By.XPATH,
            "//*[contains(.,'Get Phone') or "
            "contains(.,'Contact') or "
            "contains(.,'Phone')]"
        )

        # Wait for button clickable
        contact_button = WaitUtils.wait_for_clickable(
            driver,
            contact_locator
        )

        # Scroll to button
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            contact_button
        )

        # Slow execution before click
        WaitUtils.slow_execution(driver, 3)

        # Normal Selenium click
        contact_button.click()

        # Slow execution after click
        WaitUtils.slow_execution(driver, 5)

        # Wait for login / OTP / mobile popup
        WaitUtils.wait_for_presence(
            driver,
            (
                By.XPATH,
                "//*[contains(.,'Login') or "
                "contains(.,'Mobile') or "
                "contains(.,'OTP') or "
                "contains(.,'Phone')]"
            )
        )

        print(f"View Number button clicked successfully for {city}")



    @pytest.mark.parametrize(
        "invalid_location",
        [
            "@@@@",
            "xyz123invalid"

        ]
    )
    def test_invalid_location_search(
            self,
            base_url,
            invalid_location
    ):
        home = HomePage(self.driver)

        # Open website
        home.open(base_url)
        home.wait_for_page_load()

        WaitUtils.slow_execution(self.driver, 1)

        # Open commercial tab
        commercial = home.open_commercial_tab()

        WaitUtils.slow_execution(self.driver, 1)

        # Search invalid location
        commercial.search_commercial_property(invalid_location)

        WaitUtils.slow_execution(self.driver, 1)

        # Verify invalid search handled
        assert not commercial.is_results_loaded()

        print(f"Invalid location search handled for {invalid_location}")






    @pytest.mark.parametrize(
        "invalid_url",
        [
            "https://www.99acres.com/search/property/buy/commercial-property-in-@@@@",
            "https://www.99acres.com/search/property/buy/commercial-property-in-invalidcity123",

        ]
    )
    def test_invalid_commercial_url(
            self,
            driver,
            invalid_url
    ):
        # Open invalid commercial URL
        driver.get(invalid_url)

        driver.maximize_window()

        # Wait for page load
        WaitUtils.wait_for_page_load(driver)

        WaitUtils.slow_execution(driver, 3)

        # Verify no results / invalid page
        no_result = WaitUtils.wait_for_presence(
            driver,
            (
                By.XPATH,
                "//*[contains(.,'No Results') or "
                "contains(.,'not found') or "
                "contains(.,'0 results') or "
                "contains(.,'Try searching')]"
            )
        )

        assert no_result.is_displayed()

        print(f"Invalid URL handled correctly: {invalid_url}")

