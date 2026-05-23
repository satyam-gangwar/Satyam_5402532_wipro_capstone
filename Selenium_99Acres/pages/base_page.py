from __future__ import annotations

import time
from collections.abc import Iterable

from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from utilities.logger import get_logger

Locator = tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.explicit_wait)
        self.logger = get_logger(self.__class__.__name__)

    def open(self, url: str) -> None:
        self.logger.info("Opening URL: %s", url)
        self.driver.get(url)
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout: int | None = None) -> None:
        WebDriverWait(self.driver, timeout or settings.page_load_timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        self.logger.info("Page loaded completely: %s", self.driver.current_url)

    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_first_visible(self, locator: Locator, timeout: int | None = None) -> WebElement:
        def _visible_element(driver: WebDriver) -> WebElement | bool:
            for element in driver.find_elements(*locator):
                if element.is_displayed():
                    return element
            return False

        return WebDriverWait(self.driver, timeout or settings.explicit_wait).until(_visible_element)

    def find_clickable(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Locator) -> None:
        self.logger.info("Clicking element: %s", locator)
        self.find_clickable(locator).click()

    def js_click(self, locator: Locator) -> None:
        element = self.find_first_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_and_click(self, locator: Locator, timeout: int | None = None, retries: int = 3) -> None:
        wait_timeout = timeout or settings.explicit_wait
        for attempt in range(retries):
            try:
                element = self.find_first_visible(locator, timeout=wait_timeout)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element = WebDriverWait(self.driver, wait_timeout).until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].click();", element)
                return
            except StaleElementReferenceException:
                self.logger.info("Stale element while clicking %s. Retry %s/%s.", locator, attempt + 1, retries)
                if attempt == retries - 1:
                    raise
                time.sleep(1)
            except ElementClickInterceptedException:
                if attempt == retries - 1:
                    raise
                time.sleep(1)

    def type_text(self, locator: Locator, text: str, clear: bool = True) -> None:
        element = self.find_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        return self.find_visible(locator).text.strip()

    def is_visible(self, locator: Locator, timeout: int | None = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or settings.explicit_wait).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def click_first_available(self, locators: Iterable[Locator], timeout: int = 5, retries: int = 3) -> Locator:
        for locator in locators:
            for attempt in range(retries):
                try:
                    element = self._first_clickable(locator, timeout)
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
                    self.driver.execute_script("arguments[0].click();", element)
                    self.logger.info("Clicked available locator: %s", locator)
                    return locator
                except StaleElementReferenceException:
                    self.logger.info("Stale element while clicking %s. Retry %s/%s.", locator, attempt + 1, retries)
                    if attempt == retries - 1:
                        break
                    time.sleep(1)
                except ElementClickInterceptedException:
                    if attempt == retries - 1:
                        break
                    time.sleep(1)
                except TimeoutException:
                    break
        raise TimeoutException(f"None of the locators were clickable: {list(locators)}")

    def _first_clickable(self, locator: Locator, timeout: int) -> WebElement:
        def _clickable_element(driver: WebDriver) -> WebElement | bool:
            for element in driver.find_elements(*locator):
                if element.is_displayed() and element.is_enabled():
                    return element
            return False

        return WebDriverWait(self.driver, timeout).until(_clickable_element)

    def visible_text_present(self, text: str, timeout: int = 10) -> bool:
        xpath = (By.XPATH, f"//*[contains(normalize-space(), {self._xpath_literal(text)})]")
        return self.is_visible(xpath, timeout=timeout)

    @staticmethod
    def _xpath_literal(value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ', "\"\'\"", '.join(f"'{part}'" for part in parts) + ")"
