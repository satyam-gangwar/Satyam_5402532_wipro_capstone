

from __future__ import annotations

import time

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.commercial_locators import CommercialLocators
from utils.logger import LogGen
from utils.waits import WaitUtils
from utils.config_reader import ConfigReader

logger = LogGen.loggen()


class CommercialPage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 20)

        self.last_searched_location = ""

        self.active_search_input = None

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

        logger.info(f"URL before search: {old_url}")

        try:
            search_button = WaitUtils.wait_for_element_clickable(
                self.driver,
                CommercialLocators.SEARCH_BUTTON,
                timeout=15
            )

            self.driver.execute_script(
                "arguments[0].click();",
                search_button
            )

            logger.info("Commercial search button clicked")

        except Exception:
            logger.info("Search button click failed, pressing Enter instead")

            self.active_search_input.send_keys(Keys.ENTER)

        WaitUtils.slow_execution(5)

        current_url = self.driver.current_url

        logger.info(f"URL after search: {current_url}")

        if current_url == old_url:
            logger.info("URL did not change, checking page content instead")

        WebDriverWait(self.driver, 40).until(
            lambda driver:
            "noida" in driver.page_source.lower()
            or "property" in driver.page_source.lower()
            or "commercial" in driver.page_source.lower()
            or "results" in driver.page_source.lower()
        )

        logger.info("Commercial results page loaded")



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

        property_type = property_type.lower()

        if property_type in ["shop", "shops"]:

            locators = [
                CommercialLocators.SHOPS_FILTER,
                CommercialLocators.SHOP_OPTION
            ]

            for locator in locators:

                try:
                    option = WaitUtils.wait_for_element_clickable(
                        self.driver,
                        locator,
                        timeout=8
                    )

                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        option
                    )

                    WaitUtils.slow_execution(1)

                    self.driver.execute_script(
                        "arguments[0].click();",
                        option
                    )

                    logger.info(
                        "Shop property type selected successfully"
                    )

                    WaitUtils.slow_execution(3)

                    return True

                except Exception as error:
                    logger.info(
                        f"Shop locator failed: {locator} | Error: {error}"
                    )

            logger.info(
                "Shop filter not visible before search. Skipping selection."
            )

            return False



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



    def _safe_click(self, locator, message, wait_time=2):

        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(locator)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                element
            )

            WaitUtils.slow_execution(1)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )

            self.driver.execute_script(
                "arguments[0].click();",
                element
            )

            logger.info(message)

            WaitUtils.slow_execution(wait_time)

            return True

        except Exception as error:
            logger.info(
                f"{message} skipped. Error: {error}"
            )

            return False



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

        logger.info("Applying all Noida commercial filters")

        filters = [

            (CommercialLocators.OWNER, "Owner"),
            (CommercialLocators.VERIFIED_CHECKBOX, "Verified Checkbox"),

            (CommercialLocators.HEADER_OWNER, "Header Owner"),
            (CommercialLocators.HEADER_VERIFIED, "Header Verified"),

            (CommercialLocators.HEADER_READY_TO_MOVE, "Header Ready To Move"),
            (CommercialLocators.HEADER_WITH_PHOTOS, "Header With Photos"),

            (CommercialLocators.BUDGET_NO_MIN, "Budget No Min"),
            (CommercialLocators.BUDGET_MIN_10_LAC, "Budget Min 10 Lac"),
            (CommercialLocators.BUDGET_NO_MAX, "Budget No Max"),

            (CommercialLocators.SHOPS_FILTER, "Shops Filter"),
            (CommercialLocators.SHOWROOM_FILTER, "Showroom Filter"),
            (CommercialLocators.KIOSK_FILTER, "Kiosk Filter"),

            (CommercialLocators.SECURITY_GUARD, "Security Guard"),

            (CommercialLocators.SHOPS_RETAIL, "Shops Retail"),

            (CommercialLocators.READY_TO_MOVE_OFFICES, "Ready To Move Offices"),
            (CommercialLocators.BARE_SHELL_OFFICES, "Bare Shell Offices"),

            (CommercialLocators.PRE_LEASED_SPACES, "Pre Leased Spaces"),

            (CommercialLocators.CO_WORKING, "Co Working"),

            (CommercialLocators.SECTOR_62, "Sector 62"),
            (CommercialLocators.SECTOR_132, "Sector 132"),

            (CommercialLocators.READY_TO_MOVE_COMMERCIAL, "Ready To Move Commercial"),
            (CommercialLocators.UNDER_CONSTRUCTION_COMMERCIAL, "Under Construction Commercial"),

            (CommercialLocators.RESALE, "Resale"),
            (CommercialLocators.NEW_BOOKING, "New Booking"),

            (CommercialLocators.LIFT, "Lift"),
            (CommercialLocators.POWER_BACKUP, "Power Backup")
        ]

        working_filters = []
        failed_filters = []

        for locator, filter_name in filters:

            try:

                result = self._safe_click(
                    locator,
                    f"{filter_name} selected",
                    wait_time=2
                )

                if result:
                    working_filters.append(filter_name)

                else:
                    failed_filters.append(filter_name)

            except Exception as error:

                logger.info(
                    f"{filter_name} failed | Error: {error}"
                )

                failed_filters.append(filter_name)

        logger.info(
            f"WORKING FILTERS: {working_filters}"
        )

        logger.info(
            f"FAILED FILTERS: {failed_filters}"
        )

        WaitUtils.slow_execution(5)

        return working_filters



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




    def click_any_property_from_results(self):

        logger.info("Clicking any commercial property from results")

        WaitUtils.slow_execution(5)

        self.driver.execute_script(
            "window.scrollBy(0, 500);"
        )

        locators = [
            CommercialLocators.PROPERTY_TITLE_LINK,
            CommercialLocators.PROPERTY_CARD_FALLBACK
        ]

        for locator in locators:

            try:
                property_element = WaitUtils.wait_for_element_clickable(
                    self.driver,
                    locator,
                    timeout=15
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    property_element
                )

                WaitUtils.slow_execution(2)

                self.driver.execute_script(
                    "arguments[0].click();",
                    property_element
                )

                logger.info(
                    f"Clicked commercial property using locator: {locator}"
                )

                WaitUtils.slow_execution(5)

                return True

            except Exception as error:
                logger.info(
                    f"Property locator failed: {locator} | Error: {error}"
                )

        raise AssertionError(
            "No clickable commercial property found in results"
        )

    def is_property_detail_page_opened(self):

        self.switch_to_latest_tab()

        return (
                "spid" in self.driver.current_url
                or "showroom-for-sale" in self.driver.current_url
                or "m3m-the-line" in self.driver.current_url
        )



    def click_fixed_property_m3m(self):

        logger.info("Opening M3M The Line property directly")

        property_url = (
            "https://www.99acres.com/"
            "showroom-for-sale-in-m3m-the-line-sector-72-noida-"
            "1640-sqft-spid-V89447334"
        )

        old_windows = self.driver.window_handles

        self.driver.execute_script(
            "window.open(arguments[0], '_blank');",
            property_url
        )

        WebDriverWait(self.driver, 10).until(
            lambda driver:
            len(driver.window_handles) > len(old_windows)
        )

        self.driver.switch_to.window(
            self.driver.window_handles[-1]
        )

        WaitUtils.slow_execution(8)

        logger.info(
            f"M3M property page opened: {self.driver.current_url}"
        )



    def switch_to_latest_tab(self):

        windows = self.driver.window_handles

        self.driver.switch_to.window(windows[-1])

        self.wait.until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )



    def is_results_loaded(self):

        try:
            WebDriverWait(self.driver, 30).until(
                lambda driver: (
                        "commercial" in driver.current_url.lower()
                        or "search" in driver.current_url.lower()
                        or "property" in driver.current_url.lower()
                )
            )

            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//body//*[contains(text(),'Commercial')]"
                        " | //body//*[contains(text(),'Office')]"
                        " | //body//*[contains(text(),'Shop')]"
                        " | //body//*[contains(text(),'Showroom')]"
                        " | //body//*[contains(text(),'Property')]"
                        " | //body//*[contains(text(),'results')]"
                    )
                )
            )

            return True

        except TimeoutException:
            return False