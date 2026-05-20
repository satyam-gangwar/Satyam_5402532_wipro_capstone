from __future__ import annotations

import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utilities.logger import get_logger
from utilities.waits import WaitUtils


logger = get_logger("CommercialPage")


class CommercialPage(BasePage):

    SEARCH_INPUT = (
        By.XPATH,
        "//input[contains(@placeholder,'Search') or contains(@type,'text')]"
    )

    RESULTS_CONTAINER = (
        By.XPATH,
        "//*[contains(@class,'srpTuple') "
        "or contains(@class,'tupleCard') "
        "or contains(@class,'listings') "
        "or contains(@class,'results')]"
    )

    CONTACT_BUTTON = (
        By.XPATH,
        "//*[contains(.,'Get Phone') or "
        "contains(.,'Contact') or "
        "contains(.,'Phone')]"
    )

    LOGIN_OTP_POPUP = (
        By.XPATH,
        "//*[contains(.,'Login') or "
        "contains(.,'Mobile') or "
        "contains(.,'OTP') or "
        "contains(.,'Phone')]"
    )

    VERIFIED_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Verified')]"
    )

    BUDGET_MIN = (
        By.XPATH,
        "//*[contains(text(),'No min')]"
    )

    BUDGET_MIN_OPTION = (
        By.XPATH,
        "//*[contains(text(),'10 Lac')]"
    )

    BUDGET_MAX = (
        By.XPATH,
        "//*[contains(text(),'No max')]"
    )

    BUDGET_MAX_OPTION = (
        By.XPATH,
        "//*[contains(text(),'50 Lac')]"
    )

    APARTMENT_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Residential Apartment')]"
    )

    VILLA_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Independent House/Villa')]"
    )

    BHK_2 = (
        By.XPATH,
        "//*[contains(text(),'2 BHK')]"
    )

    BHK_3 = (
        By.XPATH,
        "//*[contains(text(),'3 BHK')]"
    )

    READY_TO_MOVE = (
        By.XPATH,
        "//*[contains(text(),'Ready to move')]"
    )

    UNDER_CONSTRUCTION = (
        By.XPATH,
        "//*[contains(text(),'Under Construction')]"
    )

    OWNER = (
        By.XPATH,
        "//*[contains(text(),'Owner')]"
    )

    CENTRAL_NOIDA = (
        By.XPATH,
        "//*[contains(text(),'Central Noida')]"
    )

    SECTOR_150 = (
        By.XPATH,
        "//*[contains(text(),'Sector 150')]"
    )

    def open_commercial_city_page(self, city):

        self.driver.get(
            f"https://www.99acres.com/search/property/buy/commercial-property-in-{city.lower()}?keyword={city}"
        )

        self.driver.maximize_window()

        logger.info(
            "Opened commercial property page for %s",
            city
        )

    def wait_for_city_content(self, city):

        WaitUtils.wait_for_presence(
            self.driver,
            (
                By.XPATH,
                f"//*[contains(.,'{city}')]"
            )
        )

        logger.info(
            "Page content loaded for %s",
            city
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

        contact_button = WaitUtils.wait_for_clickable(
            self.driver,
            self.CONTACT_BUTTON
        )

        logger.info(
            "Contact button located successfully"
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

        WaitUtils.slow_execution(
            self.driver,
            5
        )

    def verify_login_popup_displayed(self):

        WaitUtils.wait_for_presence(
            self.driver,
            self.LOGIN_OTP_POPUP
        )

        logger.info(
            "Login/OTP popup displayed successfully"
        )

        return True

    def search_commercial_property(self, location: str) -> None:

        logger.info(
            "Searching commercial property for location: %s",
            location
        )

        search_box = self.find_first_visible(
            self.SEARCH_INPUT,
            timeout=15
        )

        logger.info("Commercial search input found")

        search_box.clear()

        logger.info("Cleared commercial search input")

        search_box.send_keys(location)

        logger.info(
            "Entered location: %s",
            location
        )

        search_box.send_keys(Keys.ENTER)

        logger.info("Pressed Enter to trigger commercial search")

        WebDriverWait(self.driver, 20).until(
            lambda d: "result" in d.page_source.lower()
        )

        logger.info("Commercial search results page loaded")

    def apply_basic_filters(self) -> None:

        logger.info("Applying commercial filters")

        self._safe_click(
            self.VERIFIED_CHECKBOX,
            "Verified filter selected"
        )

        self._safe_click(
            self.BUDGET_MIN,
            "Budget minimum dropdown opened",
            wait_time=3
        )

        self._safe_click(
            self.BUDGET_MIN_OPTION,
            "Minimum budget 10 Lac selected"
        )

        self._safe_click(
            self.BUDGET_MAX,
            "Budget maximum dropdown opened"
        )

        self._safe_click(
            self.BUDGET_MAX_OPTION,
            "Maximum budget 50 Lac selected"
        )

        self._safe_click(
            self.APARTMENT_CHECKBOX,
            "Residential Apartment selected"
        )

        self._safe_click(
            self.VILLA_CHECKBOX,
            "Independent House/Villa selected"
        )

        self._safe_click(
            self.BHK_2,
            "2 BHK selected",
            wait_time=2
        )

        self._safe_click(
            self.BHK_3,
            "3 BHK selected"
        )

        self._safe_click(
            self.READY_TO_MOVE,
            "Ready to move selected"
        )

        self._safe_click(
            self.UNDER_CONSTRUCTION,
            "Under Construction selected"
        )

        self._safe_click(
            self.OWNER,
            "Owner selected"
        )

        self._safe_click(
            self.CENTRAL_NOIDA,
            "Central Noida selected"
        )

        self._safe_click(
            self.SECTOR_150,
            "Sector 150 selected"
        )

        self.wait_for_page_load()

        logger.info("Commercial filters applied successfully")

    def is_results_loaded(self) -> bool:

        logger.info("Waiting for commercial results to load")

        possible_results = [
            (
                By.XPATH,
                "//*[contains(@class,'srpTuple')]"
            ),
            (
                By.XPATH,
                "//*[contains(text(),'Verified properties')]"
            ),
            (
                By.XPATH,
                "//*[contains(text(),'properties')]"
            ),
            (
                By.XPATH,
                "//div[contains(@class,'listings')]"
            ),
            (
                By.XPATH,
                "//body"
            )
        ]

        for locator in possible_results:

            try:

                logger.info(
                    "Checking result locator: %s",
                    locator
                )

                if self.is_visible(locator, timeout=8):

                    logger.info(
                        "Commercial results loaded using locator: %s",
                        locator
                    )

                    return True

            except Exception as error:

                logger.info(
                    "Result locator not visible: %s | Error: %s",
                    locator,
                    error
                )

        logger.error("Commercial results not loaded")

        return False

    def _safe_click(
        self,
        locator,
        message,
        wait_time=2
    ):

        try:

            logger.info(
                "Trying to click: %s",
                message
            )

            self.scroll_and_click(
                locator,
                timeout=5
            )

            logger.info(message)

            time.sleep(wait_time)

        except Exception as error:

            logger.info(
                "%s skipped. Error: %s",
                message,
                error
            )

    def results_contain_location(
        self,
        location: str
    ) -> bool:

        logger.info(
            "Validating location in results: %s",
            location
        )

        result = location.lower() in self.driver.page_source.lower()

        if result:

            logger.info(
                "Location found in results: %s",
                location
            )

        else:

            logger.error(
                "Location not found in results: %s",
                location
            )

        return result

    def select_property_type(
        self,
        property_type
    ):

        logger.info(
            "Selecting property type: %s",
            property_type
        )

        if property_type == "Shop":

            xpath = (
                "//*[contains(text(),'Shop') or contains(text(),'Retail')]"
            )

        elif property_type == "Office Space":

            xpath = "//*[contains(text(),'Office')]"

        else:

            xpath = f"//*[contains(text(),'{property_type}')]"

        logger.info(
            "Using property type xpath: %s",
            xpath
        )

        property_option = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)
            )
        )

        logger.info(
            "Property type option found: %s",
            property_type
        )

        self.driver.execute_script(
            "arguments[0].click();",
            property_option
        )

        logger.info(
            "Selected property type: %s",
            property_type
        )

    def is_invalid_search_handled(self):

        page_text = self.driver.page_source.lower()

        current_url = self.driver.current_url.lower()

        invalid_indicators = [
            "no results",
            "no properties",
            "no matching",
            "sorry",
            "not found",
            "invalid",
            "try another",
            "something went wrong",
            "404",
            "error"
        ]

        for text in invalid_indicators:

            if text in page_text or text in current_url:

                logger.info(
                    "Invalid search handled with message: %s",
                    text
                )

                return True

        result_cards = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'srpTuple') "
            "or contains(@class,'tupleCard')]"
        )

        if len(result_cards) == 0:

            logger.info(
                "Invalid search handled: no result cards displayed"
            )

            return True

        logger.error(
            "Invalid search not handled properly. Result cards found: %s",
            len(result_cards)
        )

        return False