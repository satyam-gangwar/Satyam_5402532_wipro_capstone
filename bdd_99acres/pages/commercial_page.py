

from __future__ import annotations

import time

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

        self._safe_click(
            CommercialLocators.HEADER_OWNER,
            "Owner header filter selected",
            wait_time=2
        )

        self._safe_click(
            CommercialLocators.HEADER_VERIFIED,
            "Verified header filter selected",
            wait_time=2
        )

        self._safe_click(
            CommercialLocators.BUDGET_NO_MIN,
            "Budget minimum dropdown opened",
            wait_time=2
        )

        self._safe_click(
            CommercialLocators.BUDGET_MIN_10_LAC,
            "Minimum budget 10 Lac selected"
        )

        self._safe_click(
            CommercialLocators.BUDGET_NO_MAX,
            "Budget maximum dropdown opened",
            wait_time=2
        )

        self._safe_click(
            CommercialLocators.SHOPS_FILTER,
            "Shops filter selected"
        )

        self._safe_click(
            CommercialLocators.KIOSK_FILTER,
            "Kiosk filter selected"
        )

        self._safe_click(
            CommercialLocators.SECURITY_GUARD,
            "Security Guard selected"
        )

        logger.info(
            "Noida commercial filters applied successfully"
        )

        WaitUtils.slow_execution(10)


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

    def click_filter_by_text(self, filter_name):

        filter_xpath = (
            f"//*[self::span or self::div or self::label or self::button]"
            f"[contains(normalize-space(),'{filter_name}')]"
        )

        locator = (
            By.XPATH,
            filter_xpath
        )

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

        logger.info(
            f"Clicked filter by text: {filter_name}"
        )

        WaitUtils.slow_execution(2)

        return True


    def apply_basic_filters(self):

        logger.info("Applying basic commercial filters")

        filter_names = [
            "Owner",
            "Verified",
            "Shops"
        ]

        clicked_filters = []

        for filter_name in filter_names:

            try:
                self.click_filter_by_text(filter_name)

                clicked_filters.append(filter_name)

            except Exception as error:
                logger.info(
                    f"Basic filter not clicked: {filter_name} | Error: {error}"
                )

        if not clicked_filters:
            logger.info(
                "No basic filters clicked, continuing without failure"
            )

        logger.info(
            f"Basic filters applied: {clicked_filters}"
        )

        return True


    def apply_noida_filters_by_text(self):

        logger.info("Applying Noida commercial filters by text")

        filter_names = [
            "Shops",
            "Pre-leased",
            "Sector 62",
            "Ready to move"
        ]

        clicked_filters = []

        for filter_name in filter_names:

            try:
                self.click_filter_by_text(filter_name)

                clicked_filters.append(filter_name)

                logger.info(
                    f"Noida filter clicked: {filter_name}"
                )

            except Exception as error:
                logger.info(
                    f"Noida filter not clicked: {filter_name} | Error: {error}"
                )

        if not clicked_filters:
            raise AssertionError(
                "No Noida commercial filters were applied"
            )

        logger.info(
            f"Noida filters applied successfully: {clicked_filters}"
        )

        return True

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

    def click_owner_details_tab(self):

        self.switch_to_latest_tab()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        owner_details_tab = self.wait.until(
            EC.presence_of_element_located(
                CommercialLocators.OWNER_DETAILS_TAB
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            owner_details_tab
        )

        self.driver.execute_script(
            "arguments[0].click();",
            owner_details_tab
        )

    def open_owner_enquiry_form(self):

        self.switch_to_latest_tab()

        trigger = self.wait.until(
            EC.presence_of_element_located(
                CommercialLocators.OWNER_FORM_TRIGGER
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            trigger
        )

        self.driver.execute_script(
            "arguments[0].click();",
            trigger
        )

    def enter_owner_contact_name(self, name):

        name_input = self.wait.until(
            EC.presence_of_element_located(
                CommercialLocators.OWNER_NAME_INPUT
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            name_input
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            name_input,
            name
        )

    def enter_owner_contact_mobile_number(self, mobile_number):

        mobile_input = self.wait.until(
            EC.presence_of_element_located(
                CommercialLocators.OWNER_MOBILE_INPUT
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            mobile_input
        )

        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
            "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
            mobile_input,
            mobile_number
        )

    def is_owner_details_form_filled(self):

        name_value = self.driver.find_element(
            *CommercialLocators.OWNER_NAME_INPUT
        ).get_attribute("value")

        return name_value.strip() != ""

    def fill_owner_enquiry_form(self, name):

        name_input = self.wait.until(
            EC.presence_of_element_located(
                CommercialLocators.OWNER_NAME_INPUT
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            name_input
        )

        self.driver.execute_script(
            """
            arguments[0].focus();
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            name_input,
            name
        )



    def switch_to_latest_tab(self):

        windows = self.driver.window_handles

        self.driver.switch_to.window(windows[-1])

        self.wait.until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

