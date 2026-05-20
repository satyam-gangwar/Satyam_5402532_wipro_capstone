

from __future__ import annotations

import pytest
import allure

from selenium.webdriver.common.by import By

from pages.home_page import HomePage
from pages.commercial_page import CommercialPage

from utilities.waits import WaitUtils
from utilities.logger import get_logger


logger = get_logger("commercial_test")


@allure.feature("Commercial Module")
class TestCommercial:

    @pytest.mark.commercial
    def test_commercial_flow(self, base_url, test_data):

        location = test_data["property_search"]["commercial_location"]

        home = HomePage(self.driver)

        # OPEN SITE
        home.open(base_url)
        home.wait_for_page_load()

        logger.info(
            "Homepage opened successfully"
        )

        # OPEN COMMERCIAL TAB
        commercial = home.open_commercial_tab()

        logger.info(
            "Commercial tab opened successfully"
        )

        # SEARCH
        commercial.search_commercial_property(location)

        logger.info(
            "Commercial property search started for %s",
            location
        )

        # FILTER
        commercial.apply_basic_filters()

        logger.info(
            "Commercial filters applied successfully"
        )

        # VALIDATE
        assert commercial.is_results_loaded(), (
            "Commercial results failed to load"
        )

        assert commercial.results_contain_location(location), (
            f"Location '{location}' not found in results"
        )

        logger.info(
            "Commercial flow completed successfully for %s",
            location
        )

    @pytest.mark.commercial
    @pytest.mark.parametrize(
        "location",
        [
            "Mumbai",
            "Delhi",
        ]
    )
    def test_multiple_city_commercial_flow(
        self,
        base_url,
        location
    ):

        home = HomePage(self.driver)

        # OPEN SITE
        home.open(base_url)
        home.wait_for_page_load()

        logger.info(
            "Homepage opened successfully"
        )

        # OPEN COMMERCIAL TAB
        commercial = home.open_commercial_tab()

        logger.info(
            "Commercial tab opened successfully"
        )

        # SEARCH
        commercial.search_commercial_property(location)

        logger.info(
            "Commercial search triggered for %s",
            location
        )

        # FILTER
        commercial.apply_basic_filters()

        logger.info(
            "Commercial filters applied"
        )

        # VALIDATE
        assert commercial.is_results_loaded(), (
            "Commercial results failed to load"
        )

        assert commercial.results_contain_location(location), (
            f"Location '{location}' not found in results"
        )

        logger.info(
            "Commercial search successful for %s",
            location
        )

    @pytest.mark.commercial
    @pytest.mark.parametrize(
        "location, property_type",
        [
            ("Noida", "Shop")
        ]
    )
    def test_search_shop_showroom(
        self,
        base_url,
        location,
        property_type
    ):

        home = HomePage(self.driver)

        home.open(base_url)
        home.wait_for_page_load()

        WaitUtils.slow_execution(
            self.driver,
            2
        )

        logger.info(
            "Homepage loaded successfully"
        )

        commercial = home.open_commercial_tab()

        WaitUtils.slow_execution(
            self.driver,
            2
        )

        logger.info(
            "Commercial tab opened"
        )

        commercial.select_property_type(
            property_type
        )

        WaitUtils.slow_execution(
            self.driver,
            2
        )

        logger.info(
            "Selected property type: %s",
            property_type
        )

        commercial.search_commercial_property(
            location
        )

        WaitUtils.slow_execution(
            self.driver,
            3
        )

        logger.info(
            "Commercial property searched in %s",
            location
        )

        assert commercial.is_results_loaded(), (
            "Commercial results failed to load"
        )

        logger.info(
            "%s search successful in %s",
            property_type,
            location
        )

        # WAIT BEFORE CLOSING
        WaitUtils.slow_execution(
            self.driver,
            5
        )

    @pytest.mark.parametrize(
        "city",
        [
            "Noida"
        ]
    )
    def test_view_number_button(
        self,
        driver,
        city
    ):

        # OPEN PROPERTY PAGE
        driver.get(
            f"https://www.99acres.com/search/property/buy/commercial-property-in-{city.lower()}?keyword={city}"
        )

        driver.maximize_window()

        logger.info(
            "Opened commercial property page for %s",
            city
        )

        # WAIT FOR PAGE LOAD
        WaitUtils.wait_for_page_load(driver)

        WaitUtils.slow_execution(
            driver,
            2
        )

        # WAIT FOR PAGE CONTENT
        WaitUtils.wait_for_presence(
            driver,
            (
                By.XPATH,
                f"//*[contains(.,'{city}')]"
            )
        )

        logger.info(
            "Page content loaded for %s",
            city
        )

        # SCROLL DOWN
        driver.execute_script(
            "window.scrollBy(0, 800);"
        )

        WaitUtils.slow_execution(
            driver,
            2
        )

        logger.info(
            "Scrolled down successfully"
        )

        # CONTACT BUTTON
        contact_locator = (
            By.XPATH,
            "//*[contains(.,'Get Phone') or "
            "contains(.,'Contact') or "
            "contains(.,'Phone')]"
        )

        contact_button = WaitUtils.wait_for_clickable(
            driver,
            contact_locator
        )

        logger.info(
            "Contact button located successfully"
        )

        # SCROLL TO BUTTON
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            contact_button
        )

        WaitUtils.slow_execution(
            driver,
            3
        )

        # CLICK BUTTON
        contact_button.click()

        logger.info(
            "View Number button clicked successfully for %s",
            city
        )

        WaitUtils.slow_execution(
            driver,
            5
        )

        # VERIFY LOGIN POPUP
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

        logger.info(
            "Login/OTP popup displayed successfully"
        )

    @pytest.mark.parametrize(
        "invalid_location",
        [
            "@@@@",
            "xyz123invalid"
        ]
    )
    def test_invalid_location_search(
        self,
        driver,
        base_url,
        invalid_location
    ):

        home = HomePage(driver)

        home.open(base_url)
        home.wait_for_page_load()

        logger.info(
            "Homepage opened successfully"
        )

        commercial = home.open_commercial_tab()

        logger.info(
            "Commercial tab opened"
        )

        commercial.search_commercial_property(
            invalid_location
        )

        logger.info(
            "Invalid search triggered for %s",
            invalid_location
        )

        assert commercial.is_invalid_search_handled(), (
            "Invalid search was not handled properly"
        )

        logger.info(
            "Invalid location handled successfully: %s",
            invalid_location
        )

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "https://www.99acres.com/search/property/buy/commercial-property-in-@@@@",
            "https://www.99acres.com/search/property/buy/commercial-property-in-invalidcity123"
        ]
    )
    def test_invalid_commercial_url(
        self,
        driver,
        invalid_url
    ):

        driver.get(invalid_url)

        logger.info(
            "Opened invalid URL: %s",
            invalid_url
        )

        commercial = CommercialPage(driver)

        assert commercial.is_invalid_search_handled(), (
            "Invalid URL was not handled properly"
        )

        logger.info(
            "Invalid URL handled successfully: %s",
            invalid_url
        )