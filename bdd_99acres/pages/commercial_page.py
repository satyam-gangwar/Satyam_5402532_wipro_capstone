

from __future__ import annotations

import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from locators.commercial_locators import CommercialLocators
from utils.logger import LogGen
from utils.waits import WaitUtils


logger = LogGen.loggen()


class CommercialPage:

    def __init__(self, driver):

        self.driver = driver
        self.last_searched_location = ""

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

        locator = (
            CommercialLocators.CITY_TEXT[0],
            CommercialLocators.CITY_TEXT[1].format(city=city)
        )

        WaitUtils.wait_for_presence_of_element(
            self.driver,
            locator
        )

        logger.info(
            f"Page content loaded for {city}"
        )

    def scroll_to_contact_button(self):

        self.driver.execute_script(
            "window.scrollBy(0, 800);"
        )

        WaitUtils.slow_execution(2)

        logger.info(
            "Scrolled down successfully"
        )

    def click_view_number_button(self):

        contact_button = WaitUtils.wait_for_element_clickable(
            self.driver,
            CommercialLocators.CONTACT_BUTTON,
            timeout=15
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            contact_button
        )

        WaitUtils.slow_execution(2)

        self.driver.execute_script(
            "arguments[0].click();",
            contact_button
        )

        logger.info(
            "View Number button clicked successfully"
        )

    def verify_login_popup_displayed(self):

        WaitUtils.wait_for_presence_of_element(
            self.driver,
            CommercialLocators.LOGIN_OTP_POPUP,
            timeout=15
        )

        logger.info(
            "Login popup displayed successfully"
        )

        return True

    def search_commercial_property(self, location):

        self.last_searched_location = location

        logger.info(
            f"Entering commercial property location: {location}"
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

            logger.info(
                "Clicked commercial search box area"
            )

        except Exception:
            logger.info(
                "Commercial search box area click skipped"
            )

        search_inputs = self.driver.find_elements(
            *CommercialLocators.SEARCH_INPUT
        )

        visible_input = None

        for input_box in search_inputs:

            try:
                if input_box.is_displayed() and input_box.is_enabled():
                    visible_input = input_box
                    break

            except Exception:
                pass

        if visible_input is None:
            raise AssertionError(
                "No visible commercial search input found"
            )

        try:
            visible_input.clear()

        except Exception:
            logger.info(
                "Input clear skipped"
            )

        visible_input.send_keys(
            location
        )

        logger.info(
            f"Commercial location entered: {location}"
        )

        WaitUtils.slow_execution(2)

    def click_search_button(self):

        old_url = self.driver.current_url

        search_button = WaitUtils.wait_for_element_clickable(
            self.driver,
            CommercialLocators.SEARCH_BUTTON,
            timeout=15
        )

        self.driver.execute_script(
            "arguments[0].click();",
            search_button
        )

        WebDriverWait(self.driver, 40).until(
            lambda driver:
            driver.current_url != old_url
            or self.last_searched_location.lower()
            in driver.current_url.lower()
        )

        logger.info(
            f"Redirected URL: {self.driver.current_url}"
        )

    def is_results_loaded(self):

        possible_results = [
            CommercialLocators.RESULTS_CONTAINER,
            CommercialLocators.RESULTS_TEXT
        ]

        for locator in possible_results:

            try:
                WaitUtils.wait_for_element_visible(
                    self.driver,
                    locator,
                    timeout=10
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

        result = (
            location.lower()
            in self.driver.page_source.lower()
        )

        if result:
            logger.info(
                f"Location found in results: {location}"
            )

        else:
            logger.error(
                f"Location not found in results: {location}"
            )

        return result

    def select_property_type(self, property_type):

        logger.info(
            f"Selecting property type: {property_type}"
        )

        if property_type.lower() == "shop":

            option = WaitUtils.wait_for_element_clickable(
                self.driver,
                CommercialLocators.SHOP_OPTION,
                timeout=15
            )

            self.driver.execute_script(
                "arguments[0].click();",
                option
            )

            logger.info(
                "Shop property type selected"
            )

            WaitUtils.slow_execution(2)

    def is_invalid_search_handled(self):

        page_text = self.driver.page_source.lower()
        current_url = self.driver.current_url.lower()

        invalid_indicators = [
            "no results",
            "no properties",
            "not found",
            "invalid",
            "404",
            "error",
            "try another"
        ]

        for text in invalid_indicators:

            if text in page_text or text in current_url:
                logger.info(
                    f"Invalid search handled with indicator: {text}"
                )

                return True

        result_cards = self.driver.find_elements(
            *CommercialLocators.RESULT_CARDS
        )

        return len(result_cards) == 0

    def _safe_click(
        self,
        locator,
        message,
        wait_time=2
    ):

        try:
            element = WaitUtils.wait_for_element_clickable(
                self.driver,
                locator,
                timeout=5
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

            WaitUtils.slow_execution(wait_time)

        except Exception as error:
            logger.info(
                f"{message} skipped. Error: {error}"
            )

    def enter_commercial_location(self, location):

        self.last_searched_location = location

        logger.info(
            f"Entering commercial location: {location}"
        )

        search_inputs = self.driver.find_elements(
            *CommercialLocators.SEARCH_INPUT
        )

        visible_input = None

        for input_box in search_inputs:

            try:
                if input_box.is_displayed() and input_box.is_enabled():
                    visible_input = input_box
                    break

            except Exception:
                pass

        if visible_input is None:
            raise AssertionError(
                "No visible commercial search input found"
            )

        visible_input.clear()
        visible_input.send_keys(location)

        WaitUtils.slow_execution(2)

        visible_input.send_keys(Keys.ARROW_DOWN)
        visible_input.send_keys(Keys.ENTER)

        self.active_search_input = visible_input

        logger.info(
            f"Entered and selected commercial location: {location}"
        )

        WaitUtils.slow_execution(2)

    def select_location_suggestion(self):

        logger.info("Trying to select commercial location suggestion")

        dynamic_location_locator = (
            CommercialLocators.LOCATION_SUGGESTION_DYNAMIC[0],
            CommercialLocators.LOCATION_SUGGESTION_DYNAMIC[1].format(
                location=self.last_searched_location
            )
        )

        suggestion_locators = [
            dynamic_location_locator,
            CommercialLocators.SUGGESTION_BOX,
            CommercialLocators.MUMBAI_SUGGESTION
        ]

        for locator in suggestion_locators:

            try:
                suggestion = WaitUtils.wait_for_element_clickable(
                    self.driver,
                    locator,
                    timeout=5
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    suggestion
                )

                logger.info("Commercial location suggestion selected")
                return True

            except Exception:
                logger.info(f"Suggestion locator failed: {locator}")

        logger.info("No suggestion found. Continuing without suggestion.")
        return False



    def wait_for_results_page(self):

        try:
            WebDriverWait(
                self.driver,
                30
            ).until(
                lambda driver:
                "search" in driver.current_url.lower()
                or "commercial" in driver.current_url.lower()
                or "property" in driver.current_url.lower()
                or self.last_searched_location.lower()
                in driver.current_url.lower()
            )

            logger.info(
                f"Commercial results page detected: {self.driver.current_url}"
            )

            return True

        except Exception:

            logger.error(
                f"Commercial results page not detected. Current URL: {self.driver.current_url}"
            )

            return False

    def apply_noida_filters(self):

        logger.info("Applying Noida commercial filters")

        worked_filters = []
        failed_filters = []

        filter_steps = [

            (
                CommercialLocators.BUDGET_NO_MIN,
                "Budget No Min"
            ),

            (
                CommercialLocators.BUDGET_MIN_10_LAC,
                "Min Budget 10 Lac"
            ),

            (
                CommercialLocators.BUDGET_NO_MAX,
                "Budget No Max"
            ),

            (
                CommercialLocators.SECURITY_GUARD,
                "Security Guard"
            ),




        ]

        for locator, filter_name in filter_steps:

            try:

                logger.info(f"Trying filter: {filter_name}")

                element = WaitUtils.wait_for_element_clickable(
                    self.driver,
                    locator,
                    timeout=10
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    element
                )

                WaitUtils.slow_execution(1)

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

                WaitUtils.slow_execution(3)

                self.driver.execute_script(
                    "window.scrollTo(0, 0);"
                )

                logger.info(f"Filter applied: {filter_name}")

                worked_filters.append(filter_name)

            except Exception as error:

                logger.error(
                    f"Filter failed: {filter_name} | Error: {error}"
                )

                failed_filters.append(filter_name)

        logger.info(f"WORKING FILTERS: {worked_filters}")

        logger.info(f"FAILED FILTERS: {failed_filters}")



    def click_filter_and_verify(self, locator, filter_name):

        element = WaitUtils.wait_for_element_clickable(
            self.driver,
            locator,
            timeout=15
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        WaitUtils.slow_execution(2)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        WaitUtils.slow_execution(3)

        page_source = self.driver.page_source.lower()

        if filter_name.lower() in page_source:
            logger.info(f"Filter visible on page after click: {filter_name}")
            return True

        logger.error(f"Filter not visible after click: {filter_name}")
        return False

    def click_filter_and_return_top(self, locator, filter_name):

        element = WaitUtils.wait_for_element_clickable(
            self.driver,
            locator,
            timeout=15
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        WaitUtils.slow_execution(1)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        logger.info(f"Clicked filter: {filter_name}")

        WaitUtils.slow_execution(2)

        self.driver.execute_script(
            "window.scrollTo(0, 0);"
        )

        WaitUtils.slow_execution(3)

    def is_filter_applied_on_screen(self, filter_name):

        applied_xpath = (
            f"//*[contains(@class,'tag') "
            f"or contains(@class,'chip') "
            f"or contains(@class,'applied') "
            f"or contains(@class,'selected')]"
            f"[contains(normalize-space(),'{filter_name}')]"
        )

        return len(
            self.driver.find_elements(By.XPATH, applied_xpath)
        ) > 0
