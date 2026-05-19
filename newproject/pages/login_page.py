from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from pages.base_page import BasePage, Locator


class LoginSessionExpiredError(RuntimeError):
    pass


class LoginPage(BasePage):
    SESSION_EXPIRED_MESSAGE: Locator = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Your session has been expired') or contains(normalize-space(), 'session has been expired')]",
    )
    MOBILE_NUMBER_INPUTS: tuple[Locator, ...] = (
        (By.XPATH, "//input[@data-for='phnNumber']"),
        (By.XPATH, "//input[@placeholder='Phone Number']"),
        (By.XPATH, "//input[@title='Phone Number']"),
        (By.XPATH, "//input[@type='tel' or contains(@placeholder, 'Phone')]"),
    )
    MOBILE_NUMBER_INPUT: Locator = MOBILE_NUMBER_INPUTS[0]
    CONTINUE_BUTTONS: tuple[Locator, ...] = (
        (By.XPATH, "//button[normalize-space()='Continue']"),
        (By.XPATH, "//*[@id='app']/div/div[7]/div[2]/div[1]/div/div/form/div[2]/button"),
    )
    USERNAME_FIELDS: tuple[Locator, ...] = (
        (By.XPATH, "//input[@type='tel' or @type='email' or contains(@placeholder, 'Mobile') or contains(@placeholder, 'Email')]"),
        (By.CSS_SELECTOR, "input[type='text']"),
    )
    PASSWORD_FIELDS: tuple[Locator, ...] = (
        (By.XPATH, "//input[@type='password']"),
    )
    LOGIN_DIALOG = (
        By.XPATH,
        "//*[contains(., 'Login') or contains(., 'LOGIN / REGISTER') or contains(., 'Mobile') or contains(., 'Email')][self::div or self::section or self::form]",
    )

    def is_login_dialog_displayed(self) -> bool:
        return self.is_visible(self.LOGIN_DIALOG, timeout=10)

    def is_session_expired_message_displayed(self) -> bool:
        return self.is_visible(self.SESSION_EXPIRED_MESSAGE, timeout=3)

    def submit_username(self, username: str) -> None:
        if not username:
            raise ValueError("Username is required for login.")
        self._type_into_first_available(self.USERNAME_FIELDS, username)
        self.click_first_available(self.CONTINUE_BUTTONS)

    def start_mobile_login_and_pause_for_otp(
        self,
        mobile_number: str,
        otp_pause_seconds: int = 60,
        before_mobile_entry_pause_seconds: int = 0,
        after_mobile_entry_pause_seconds: int = 0,
    ) -> None:
        if not mobile_number:
            raise ValueError("Mobile number is required for login.")

        if before_mobile_entry_pause_seconds > 0:
            self.logger.info(
                "Paused for %s seconds before entering mobile number.",
                before_mobile_entry_pause_seconds,
            )
            time.sleep(before_mobile_entry_pause_seconds)
        self.enter_mobile_number(mobile_number)
        if after_mobile_entry_pause_seconds > 0:
            self.logger.info(
                "Paused for %s seconds after entering mobile number.",
                after_mobile_entry_pause_seconds,
            )
            time.sleep(after_mobile_entry_pause_seconds)
        if self.is_session_expired_message_displayed():
            raise LoginSessionExpiredError("99acres login session expired before Continue was clicked.")
        self.click_first_available(self.CONTINUE_BUTTONS, timeout=10)
        if self.is_session_expired_message_displayed():
            raise LoginSessionExpiredError("99acres login session expired after Continue was clicked.")
        self.logger.info("Paused for %s seconds so OTP can be entered manually.", otp_pause_seconds)
        time.sleep(otp_pause_seconds)

    def submit_password_if_present(self, password: str) -> None:
        for locator in self.PASSWORD_FIELDS:
            if self.is_visible(locator, timeout=5):
                self.type_text(locator, password)
                self.click_first_available(self.CONTINUE_BUTTONS)
                return
        self.logger.info("Password field was not shown. Site may require OTP-based login.")

    def enter_mobile_number(self, mobile_number: str) -> None:
        locator = self._first_visible_locator(self.MOBILE_NUMBER_INPUTS, timeout=10)
        self.logger.info("Entering mobile number using locator: %s", locator)
        element = self.find_first_visible(locator, timeout=10)
        WebDriverWait(self.driver, settings.explicit_wait).until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        self.driver.execute_script("arguments[0].focus();", element)
        self.driver.execute_script("arguments[0].value='';", element)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", element)
        element.send_keys(mobile_number)

    def _first_visible_locator(self, locators: tuple[Locator, ...], timeout: int = 5) -> Locator:
        for locator in locators:
            if self.is_visible(locator, timeout=timeout):
                return locator
        raise AssertionError(f"No visible element was available for locators: {locators}")

    def _type_into_first_available(self, locators: tuple[Locator, ...], text: str) -> None:
        for locator in locators:
            if self.is_visible(locator, timeout=5):
                self.type_text(locator, text)
                return
        raise AssertionError(f"No input field was available for locators: {locators}")
