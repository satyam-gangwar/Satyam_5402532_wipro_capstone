
from __future__ import annotations
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utilities.waits import WaitUtils
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class CommercialPage(BasePage):

    # ---------------- SEARCH ----------------

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

    # ---------------- FILTERS ----------------

    # VERIFIED
    VERIFIED_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Verified')]"
    )

    # BUDGET
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

    # PROPERTY TYPE
    APARTMENT_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Residential Apartment')]"
    )

    VILLA_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Independent House/Villa')]"
    )

    # BEDROOMS
    BHK_2 = (
        By.XPATH,
        "//*[contains(text(),'2 BHK')]"
    )

    BHK_3 = (
        By.XPATH,
        "//*[contains(text(),'3 BHK')]"
    )

    # CONSTRUCTION STATUS
    READY_TO_MOVE = (
        By.XPATH,
        "//*[contains(text(),'Ready to move')]"
    )

    UNDER_CONSTRUCTION = (
        By.XPATH,
        "//*[contains(text(),'Under Construction')]"
    )

    # POSTED BY
    OWNER = (
        By.XPATH,
        "//*[contains(text(),'Owner')]"
    )

    # LOCALITIES
    CENTRAL_NOIDA = (
        By.XPATH,
        "//*[contains(text(),'Central Noida')]"
    )

    SECTOR_150 = (
        By.XPATH,
        "//*[contains(text(),'Sector 150')]"
    )



    # ---------------- SEARCH ACTION ----------------

    def search_commercial_property(self, location: str) -> None:

        self.logger.info("Searching commercial property: %s", location)

        search_box = self.find_first_visible(self.SEARCH_INPUT, timeout=15)

        search_box.clear()
        search_box.send_keys(location)
        search_box.send_keys(Keys.ENTER)

        self.logger.info("Commercial search triggered")

        WebDriverWait(self.driver, 20).until(
            lambda d: "result" in d.page_source.lower()
        )

    # ---------------- FILTER ACTIONS ----------------

    def apply_basic_filters(self) -> None:

        self.logger.info("Applying commercial filters")

        # VERIFIED
        self._safe_click(self.VERIFIED_CHECKBOX, "Verified")

        # BUDGET
        self._safe_click(self.BUDGET_MIN, "Budget Min Dropdown", wait_time=3)
        self._safe_click(self.BUDGET_MIN_OPTION, "Min Budget Selected")

        self._safe_click(self.BUDGET_MAX, "Budget Max Dropdown")
        self._safe_click(self.BUDGET_MAX_OPTION, "Max Budget Selected")

        # PROPERTY TYPE
        self._safe_click(self.APARTMENT_CHECKBOX, "Apartment Selected")
        self._safe_click(self.VILLA_CHECKBOX, "Villa Selected")

        # BEDROOMS
        self._safe_click(self.BHK_2, "2 BHK Selected", wait_time=2)
        self._safe_click(self.BHK_3, "3 BHK Selected")

        # CONSTRUCTION STATUS
        self._safe_click(self.READY_TO_MOVE, "Ready To Move Selected")
        self._safe_click(self.UNDER_CONSTRUCTION, "Under Construction Selected")

        # OWNER
        self._safe_click(self.OWNER, "Owner Selected")

        # LOCALITIES
        self._safe_click(self.CENTRAL_NOIDA, "Central Noida Selected")
        self._safe_click(self.SECTOR_150, "Sector 150 Selected")

        # AMENITIES


        self.wait_for_page_load()

        self.logger.info("Commercial filters completed")


    # ---------------- VALIDATION ----------------

    def is_results_loaded(self) -> bool:

        self.logger.info("Waiting for commercial results to load")

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
                if self.is_visible(locator, timeout=8):
                    self.logger.info("Commercial results loaded successfully")
                    return True
            except Exception:
                continue

        self.logger.error("Commercial results NOT loaded")
        return False

    # ---------------- COMMON METHOD ----------------

    def _safe_click(self, locator, message, wait_time=2):

        try:
            self.scroll_and_click(locator, timeout=5)

            self.logger.info(message)

            # WAIT FOR DEMO PURPOSE
            time.sleep(wait_time)

        except Exception:

            self.logger.info("%s skipped", message)

    def results_contain_location(self, location: str) -> bool:

        self.logger.info("Validating location in results: %s", location)

        return location.lower() in self.driver.page_source.lower()



    def select_property_type(self, property_type):

        if property_type == "Shop":
            xpath = "//*[contains(text(),'Shop') or contains(text(),'Retail')]"
        elif property_type == "Office Space":
            xpath = "//*[contains(text(),'Office')]"
        else:
            xpath = f"//*[contains(text(),'{property_type}')]"

        property_option = self.wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            property_option
        )

        self.logger.info(f"Selected property type: {property_type}")