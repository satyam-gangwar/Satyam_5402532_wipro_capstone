


from __future__ import annotations

from pages.commercial_page import CommercialPage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from config.settings import settings
from pages.base_page import BasePage, Locator
from utilities.logger import get_logger

logger = get_logger("HomePage")


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
        logger.info("Loading home page using base URL: %s", settings.base_url)

        self.open(settings.base_url)

        logger.info("Home page loaded successfully")

        self.accept_cookies_if_present()

    def open(self, url: str) -> None:
        logger.info("Opening URL: %s", url)

        super().open(url)

        logger.info("Page opened successfully: %s", self.driver.current_url)

        self.accept_cookies_if_present()

    def accept_cookies_if_present(self) -> None:
        logger.info("Checking cookie confirmation popup")

        try:
            self.click_first_available(
                (self.COOKIE_OK_BUTTON,),
                timeout=3
            )

            logger.info("Cookie confirmation accepted")

        except Exception:
            logger.info("Cookie confirmation was not shown")

    def open_login(self) -> None:
        logger.info("Opening login popup")

        icon = self.find_first_visible(
            self.LOGIN_ICON,
            timeout=20
        )

        ActionChains(self.driver).move_to_element(icon).perform()

        logger.info("Hovered on login icon")

        self.click(self.LOGIN_OPTION)

        logger.info("Clicked login/register option")

    def open_commercial_tab(self) -> CommercialPage:
        logger.info("Opening Commercial tab")

        commercial_locators = [
            (By.XPATH, "//div[contains(text(),'Commercial')]"),
            (By.XPATH, "//span[contains(text(),'Commercial')]"),
            (By.XPATH, "//a[contains(text(),'Commercial')]"),
            (By.XPATH, "//*[contains(text(),'Commercial')]"),
        ]

        commercial_tab = None

        for locator in commercial_locators:
            try:
                logger.info("Trying Commercial tab locator: %s", locator)

                commercial_tab = self.find_first_visible(locator, timeout=5)

                logger.info("Commercial tab found using locator: %s", locator)

                break

            except Exception:
                logger.info("Commercial tab locator not found: %s", locator)

        if commercial_tab is None:
            logger.error("Commercial tab not found on homepage")
            raise AssertionError("Commercial tab not found on homepage")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            commercial_tab
        )

        logger.info("Scrolled to Commercial tab")

        self.driver.execute_script(
            "arguments[0].click();",
            commercial_tab
        )

        logger.info("Commercial tab opened successfully")

        return CommercialPage(self.driver)

    def search_property_from_landmark_bar(
        self,
        location: str
    ) -> None:

        logger.info("Searching property from landmark bar for: %s", location)

        try:
            self.find_first_visible(
                self.LANDMARK_SEARCH_BAR,
                timeout=10
            )

            logger.info("Landmark search bar is visible")

        except TimeoutException:

            current_url = self.driver.current_url.lower()

            logger.info(
                "Landmark search bar not visible. Current URL: %s",
                current_url
            )

            if (
                "search/property" in current_url
                and location.lower() in self.driver.page_source.lower()
            ):
                logger.info(
                    "Already on %s search results page",
                    location
                )
                return

            logger.error("Landmark search bar not found")
            raise

        search_box = self.find_first_visible(
            self.LANDMARK_SEARCH_INPUT
        )

        logger.info("Typing location in landmark search input: %s", location)

        search_box.clear()
        search_box.send_keys(location)

        logger.info("Selecting location suggestion: %s", location)

        self.click_first_available(
            (
                (
                    By.XPATH,
                    f"//*[@id='suggestions_custom']/li[@title={self._xpath_literal(location)}]"
                ),
            ),
            timeout=10,
        )

        logger.info("Clicked location suggestion")

        self.click_first_available(
            (self.SEARCH_ICON_BY_ID,),
            timeout=10
        )

        logger.info("Clicked search icon")

    def are_primary_menu_items_visible(
        self,
        expected_items: list[str] | tuple[str, ...]
    ) -> bool:

        logger.info(
            "Checking primary menu items visibility: %s",
            expected_items
        )

        missing_items = [
            item
            for item in expected_items
            if not self.visible_text_present(item, timeout=5)
        ]

        if missing_items:
            logger.error(
                "Missing primary menu items: %s",
                missing_items
            )
        else:
            logger.info("All primary menu items are visible")

        return not missing_items