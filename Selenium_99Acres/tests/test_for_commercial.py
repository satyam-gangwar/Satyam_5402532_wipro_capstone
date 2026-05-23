from __future__ import annotations

import pytest
import allure

from selenium.webdriver.common.by import By

from pages.home_page import HomePage
from pages.commercial_page import CommercialPage

from utilities.waits import WaitUtils
from utilities.logger import get_logger
from utilities.screenshot_utils import capture_screenshot


logger = get_logger("commercial_test")


@allure.feature("Commercial Module")
class TestCommercial:

    def attach_screenshot(self, name):

        screenshot_path = capture_screenshot(
            self.driver,
            name
        )

        allure.attach.file(
            screenshot_path,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

        logger.info(
            "Screenshot captured: %s",
            screenshot_path
        )

    @pytest.mark.commercial
    def test_commercial_flow(self, base_url, test_data):

        location = test_data["property_search"]["commercial_location"]

        home = HomePage(self.driver)

        home.open(base_url)
        home.wait_for_page_load()

        self.attach_screenshot("01_homepage_loaded")

        commercial = home.open_commercial_tab()

        self.attach_screenshot("02_commercial_tab_opened")

        commercial.search_commercial_property(location)

        self.attach_screenshot("03_commercial_search_results")

        commercial.apply_basic_filters()

        self.attach_screenshot("04_commercial_filters_applied")

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
            "Mumbai"

        ]
    )
    def test_multiple_city_commercial_flow(
        self,
        base_url,
        location
    ):

        home = HomePage(self.driver)

        home.open(base_url)
        home.wait_for_page_load()

        self.attach_screenshot("01_homepage_loaded")

        commercial = home.open_commercial_tab()

        self.attach_screenshot("02_commercial_tab_opened")

        commercial.search_commercial_property(location)

        self.attach_screenshot(
            f"03_commercial_search_results_{location}"
        )

        commercial.apply_basic_filters()

        self.attach_screenshot(
            f"04_commercial_filters_applied_{location}"
        )

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
            ("Noida", "Shop"),
            ("Delhi", "Shop")
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

        self.attach_screenshot("01_homepage_loaded")

        WaitUtils.slow_execution(
            self.driver,
            2
        )

        commercial = home.open_commercial_tab()

        self.attach_screenshot("02_commercial_tab_opened")

        WaitUtils.slow_execution(
            self.driver,
            2
        )

        commercial.select_property_type(
            property_type
        )

        self.attach_screenshot(
            f"03_property_type_selected_{property_type}"
        )

        WaitUtils.slow_execution(
            self.driver,
            2
        )

        commercial.search_commercial_property(
            location
        )

        self.attach_screenshot(
            f"04_{property_type}_search_results_{location}"
        )

        WaitUtils.slow_execution(
            self.driver,
            3
        )

        assert commercial.is_results_loaded(), (
            "Commercial results failed to load"
        )

        logger.info(
            "%s search successful in %s",
            property_type,
            location
        )

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

        commercial = CommercialPage(driver)

        commercial.open_commercial_city_page(city)

        WaitUtils.wait_for_page_load(driver)

        self.attach_screenshot(
            f"01_commercial_city_page_{city}"
        )

        WaitUtils.slow_execution(
            driver,
            2
        )

        commercial.wait_for_city_content(city)

        commercial.scroll_to_contact_button()

        self.attach_screenshot(
            f"02_contact_button_visible_{city}"
        )

        commercial.click_view_number_button()

        self.attach_screenshot(
            f"03_view_number_clicked_{city}"
        )

        assert commercial.verify_login_popup_displayed(), (
            "Login/OTP popup was not displayed after clicking View Number"
        )

        self.attach_screenshot(
            f"04_login_popup_displayed_{city}"
        )

    @pytest.mark.parametrize(
        "invalid_location",
        [

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

        self.attach_screenshot(
            "01_homepage_loaded_invalid_search"
        )

        commercial = home.open_commercial_tab()

        self.attach_screenshot(
            "02_commercial_tab_opened_invalid_search"
        )

        commercial.search_commercial_property(
            invalid_location
        )

        self.attach_screenshot(
            f"03_invalid_search_result_{invalid_location}"
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

        WaitUtils.wait_for_page_load(driver)

        self.attach_screenshot(
            "01_invalid_commercial_url_loaded"
        )

        commercial = CommercialPage(driver)

        assert commercial.is_invalid_search_handled(), (
            "Invalid URL was not handled properly"
        )

        self.attach_screenshot(
            "02_invalid_url_handled"
        )

        logger.info(
            "Invalid URL handled successfully: %s",
            invalid_url
        )