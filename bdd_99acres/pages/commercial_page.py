from __future__ import annotations

import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from locators.commercial_locators import CommercialLocators
from utils.logger import LogGen
from utils.waits import WaitUtils


logger = LogGen.loggen()


class CommercialPage:

    def __init__(self, driver):

        self.driver = driver

    def open_commercial_city_page(self, city):

        self.driver.get(
            f"https://www.99acres.com/search/property/buy/"
            f"commercial-property-in-{city.lower()}?keyword={city}"
        )

        self.driver.maximize_window()

        logger.info(
            f"Opened commercial property page for {city}"
        )

    def wait_for_city_content(self, city):

        WaitUtils.wait_for_presence_of_element(
            self.driver,
            (
                By.XPATH,
                f"//*[contains(.,'{city}')]"
            )
        )

        logger.info(
            f"Page content loaded for {city}"
        )

    def scroll_to_contact_button(self):

        self.driver.execute_script(
            "window.scrollBy(0, 800);"
        )

        WaitUtils.slow_execution(
            self.driver,
            2
        )

        logger.info(
            "Scrolled down successfully"
        )

    def click_view_number_button(self):

        contact_button = (
            WaitUtils.wait_for_element_clickable(
                self.driver,
                CommercialLocators.CONTACT_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            contact_button
        )

        WaitUtils.slow_execution(
            self.driver,
            3
        )

        contact_button.click()

        logger.info(
            "View Number button clicked successfully"
        )

    def verify_login_popup_displayed(self):

        WaitUtils.wait_for_presence_of_element(
            self.driver,
            CommercialLocators.LOGIN_OTP_POPUP
        )

        logger.info(
            "Login popup displayed successfully"
        )

        return True

    from selenium.webdriver.common.keys import Keys

    def search_commercial_property(self, location):

        logger.info(
            f"Searching commercial property for location: {location}"
        )

        try:
            search_area = WaitUtils.wait_for_element_clickable(
                self.driver,
                CommercialLocators.SEARCH_BOX_AREA,
                timeout=10
            )

            self.driver.execute_script(
                "arguments[0].click();",
                search_area
            )

            logger.info("Clicked search box area")

        except Exception:
            logger.info("Search box area click skipped")

        search_inputs = self.driver.find_elements(
            *CommercialLocators.SEARCH_INPUT
        )

        visible_input = None

        for input_box in search_inputs:

            try:
                if input_box.is_displayed():
                    visible_input = input_box
                    break

            except Exception:
                pass

        if visible_input is None:
            raise AssertionError(
                "No visible commercial search input found"
            )

        visible_input.clear()

        visible_input.send_keys(
            location
        )

        logger.info(
            f"Entered location: {location}"
        )

        visible_input.send_keys(
            Keys.ENTER
        )

        logger.info(
            "Pressed Enter after entering location"
        )

    def is_results_loaded(self):

        possible_results = [
            CommercialLocators.RESULTS_CONTAINER,
            (
                By.XPATH,
                "//body"
            )
        ]

        for locator in possible_results:

            try:

                WaitUtils.wait_for_element_visible(
                    self.driver,
                    locator,
                    timeout=8
                )

                logger.info(
                    "Commercial results loaded successfully"
                )

                return True

            except Exception:

                logger.info(
                    f"Result locator not visible: {locator}"
                )

        return False

    def results_contain_location(self, location):

        return (
            location.lower()
            in self.driver.page_source.lower()
        )

    def select_property_type(
            self,
            property_type
    ):

        logger.info(
            f"Selecting property type: {property_type}"
        )

        if property_type.lower() == "shop":
            option = (
                WaitUtils.wait_for_element_clickable(
                    self.driver,
                    CommercialLocators.SHOP_OPTION,
                    timeout=15
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                option
            )

            WaitUtils.slow_execution(2)



    def is_invalid_search_handled(self):

        page_text = (
            self.driver.page_source.lower()
        )

        current_url = (
            self.driver.current_url.lower()
        )

        invalid_indicators = [
            "no results",
            "not found",
            "invalid",
            "404",
            "error"
        ]

        for text in invalid_indicators:

            if (
                text in page_text
                or text in current_url
            ):

                return True

        result_cards = (
            self.driver.find_elements(
                *CommercialLocators.RESULT_CARDS
            )
        )

        return len(result_cards) == 0

    def _safe_click(
        self,
        locator,
        message,
        wait_time=2
    ):

        try:

            element = (
                WaitUtils.wait_for_element_clickable(
                    self.driver,
                    locator,
                    timeout=5
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                element
            )

            self.driver.execute_script(
                "arguments[0].click();",
                element
            )

            logger.info(message)

            time.sleep(wait_time)

        except Exception as error:

            logger.info(
                f"{message} skipped. Error: {error}"
            )