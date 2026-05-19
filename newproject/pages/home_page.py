
from __future__ import annotations

from pages.commercial_page import CommercialPage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from config.settings import settings
from pages.base_page import BasePage, Locator


class HomePage(BasePage):

    COOKIE_OK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Okay' or normalize-space()='OK']"
    )

    LOGIN_ICON = (
        By.XPATH,
        "//i[contains(@class,'icon_userWhite') and contains(@class,'theader__dot')]"
    )

    LOGIN_OPTION = (
        By.XPATH,
        "//*[contains(text(),'LOGIN / REGISTER') or "
        "contains(text(),'Login / Register') or "
        "contains(text(),'LOGIN/REGISTER') or "
        "contains(text(),'Login/Register')]",
    )

    LANDMARK_SEARCH_BAR = (
        By.XPATH,
        '//*[@id="d_landmark_inPageSearchBox"]'
    )

    LANDMARK_SEARCH_INPUT = (
        By.XPATH,
        '//*[@id="d_landmark_inPageSearchBox"]//input'
    )

    SEARCH_ICON_BY_ID = (
        By.XPATH,
        '//*[@id="searchform_search_btn"]'
    )

    LOGIN_ENTRY_POINTS: tuple[Locator, ...] = (
        (By.CSS_SELECTOR, "[data-label='USER_PROFILE_DROPDOWN']"),
        (By.CSS_SELECTOR, "[data-label='LR.INITIATE']"),
        (By.CSS_SELECTOR, ".hmenu__loginRegister"),
        (By.XPATH, "//a[contains(., 'Login') or contains(., 'login')]"),
        (By.XPATH, "//button[contains(., 'Login') or contains(., 'login')]"),
        (By.XPATH, "//*[contains(@class, 'login') or contains(@id, 'login')]"),
    )

    SEARCH_INPUTS: tuple[Locator, ...] = (
        (By.ID, "keyword2"),
        (By.CSS_SELECTOR, "#d_landmark_inPageSearchBox input[name='keyword']"),
        (By.CSS_SELECTOR, ".inPageSearchBox__searchFieldInput input"),
        (
            By.XPATH,
            "//input[contains(@placeholder, 'Search') or "
            "contains(@placeholder, 'City') or "
            "contains(@placeholder, 'Locality')]"
        ),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.XPATH, "//*[@contenteditable='true']"),
    )

    SEARCH_BUTTONS: tuple[Locator, ...] = (
        (By.ID, "searchform_search_btn"),
        (By.XPATH, "//button[contains(., 'Search')]"),
        (
            By.XPATH,
            "//*[self::button or self::a]"
            "[contains(@class, 'search') or contains(@id, 'search')]"
        ),
    )

    def load(self) -> None:
        self.open(settings.base_url)
        self.accept_cookies_if_present()

    def open(self, url: str) -> None:
        super().open(url)
        self.accept_cookies_if_present()

    def accept_cookies_if_present(self) -> None:
        try:
            self.click_first_available(
                (self.COOKIE_OK_BUTTON,),
                timeout=3
            )
        except Exception:
            self.logger.info("Cookie confirmation was not shown.")

    def open_login(self) -> None:
        icon = self.find_first_visible(
            self.LOGIN_ICON,
            timeout=30
        )

        ActionChains(self.driver).move_to_element(icon).perform()

        self.logger.info(
            "Hovered on login icon: %s",
            self.LOGIN_ICON
        )

        self.click(self.LOGIN_OPTION)

    def open_commercial_tab(self) -> CommercialPage:
        self.logger.info("Opening Commercial tab")

        commercial_locators = [
            (By.XPATH, "//div[contains(text(),'Commercial')]"),
            (By.XPATH, "//span[contains(text(),'Commercial')]"),
            (By.XPATH, "//a[contains(text(),'Commercial')]"),
            (By.XPATH, "//*[contains(text(),'Commercial')]"),
        ]

        commercial_tab = None

        for locator in commercial_locators:
            try:
                commercial_tab = self.find_first_visible(locator, timeout=5)

                self.logger.info(f"Commercial tab found using: {locator}")

                break

            except Exception:
                continue

        if commercial_tab is None:
            raise AssertionError("Commercial tab not found on homepage")

        # Scroll to element
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            commercial_tab
        )

        # Click with JS
        self.driver.execute_script(
            "arguments[0].click();",
            commercial_tab
        )

        self.logger.info("Commercial tab opened successfully")

        return CommercialPage(self.driver)

    def search_property_from_landmark_bar(
        self,
        location: str
    ) -> None:

        try:
            self.find_first_visible(
                self.LANDMARK_SEARCH_BAR,
                timeout=10
            )

        except TimeoutException:

            current_url = self.driver.current_url.lower()

            if (
                "search/property" in current_url
                and location.lower() in self.driver.page_source.lower()
            ):
                self.logger.info(
                    "Landmark search bar was not visible because "
                    "current page is already a %s results page.",
                    location,
                )
                return

            raise

        search_box = self.find_first_visible(
            self.LANDMARK_SEARCH_INPUT
        )

        search_box.clear()
        search_box.send_keys(location)

        self.click_first_available(
            (
                (
                    By.XPATH,
                    f"//*[@id='suggestions_custom']/li[@title={self._xpath_literal(location)}]"
                ),
            ),
            timeout=10,
        )

        self.click_first_available(
            (self.SEARCH_ICON_BY_ID,),
            timeout=10
        )

    def are_primary_menu_items_visible(
        self,
        expected_items: list[str] | tuple[str, ...]
    ) -> bool:

        missing_items = [
            item
            for item in expected_items
            if not self.visible_text_present(item, timeout=5)
        ]

        if missing_items:
            self.logger.error(
                "Missing primary menu items: %s",
                missing_items
            )

        return not missing_items