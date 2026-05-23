
from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from pages.base_page import BasePage, Locator
from utilities.logger import get_logger

logger = get_logger("LoginPage")


class LoginSessionExpiredError(RuntimeError):
    pass


class LoginPage(BasePage):

    SESSION_EXPIRED_MESSAGE: Locator = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Your session has been expired') "
        "or contains(normalize-space(), 'session has been expired')]",
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
        (
            By.XPATH,
            "//input[@type='tel' or @type='email' "
            "or contains(@placeholder, 'Mobile') "
            "or contains(@placeholder, 'Email')]"
        ),
        (By.CSS_SELECTOR, "input[type='text']"),
    )

    PASSWORD_FIELDS: tuple[Locator, ...] = (
        (By.XPATH, "//input[@type='password']"),
    )

    LOGIN_DIALOG = (
        By.XPATH,
        "//*[contains(., 'Login') "
        "or contains(., 'LOGIN / REGISTER') "
        "or contains(., 'Mobile') "
        "or contains(., 'Email')]"
        "[self::div or self::section or self::form]",
    )

    def is_login_dialog_displayed(self) -> bool:

        logger.info("Checking whether login dialog is displayed")

        return self.is_visible(self.LOGIN_DIALOG, timeout=10)

    def is_session_expired_message_displayed(self) -> bool:

        logger.info("Checking whether session expired message is displayed")

        return self.is_visible(self.SESSION_EXPIRED_MESSAGE, timeout=3)

    def submit_username(self, username: str) -> None:

        logger.info("Submitting username for login")

        if not username:
            logger.error("Username is missing")
            raise ValueError("Username is required for login.")

        self._type_into_first_available(self.USERNAME_FIELDS, username)

        logger.info("Username entered successfully")

        self.click_first_available(self.CONTINUE_BUTTONS)

        logger.info("Clicked Continue button after username entry")

    def start_mobile_login_and_pause_for_otp(
        self,
        mobile_number: str,
        otp_pause_seconds: int = 60,
        before_mobile_entry_pause_seconds: int = 0,
        after_mobile_entry_pause_seconds: int = 0,
    ) -> None:

        logger.info("Starting mobile login flow")

        if not mobile_number:
            logger.error("Mobile number is missing")
            raise ValueError("Mobile number is required for login.")

        if before_mobile_entry_pause_seconds > 0:
            logger.info(
                "Waiting %s seconds before entering mobile number",
                before_mobile_entry_pause_seconds,
            )
            time.sleep(before_mobile_entry_pause_seconds)

        self.enter_mobile_number(mobile_number)

        logger.info("Mobile number entered successfully")

        if after_mobile_entry_pause_seconds > 0:
            logger.info(
                "Waiting %s seconds after entering mobile number",
                after_mobile_entry_pause_seconds,
            )
            time.sleep(after_mobile_entry_pause_seconds)

        if self.is_session_expired_message_displayed():
            logger.error("Session expired before Continue button click")
            raise LoginSessionExpiredError(
                "99acres login session expired before Continue was clicked."
            )

        self.click_first_available(self.CONTINUE_BUTTONS, timeout=10)

        logger.info("Clicked Continue button")

        if self.is_session_expired_message_displayed():
            logger.error("Session expired after Continue button click")
            raise LoginSessionExpiredError(
                "99acres login session expired after Continue was clicked."
            )

        logger.info(
            "Waiting %s seconds for manual OTP entry",
            otp_pause_seconds,
        )

        time.sleep(otp_pause_seconds)

    def submit_password_if_present(self, password: str) -> None:

        logger.info("Checking whether password field is present")

        for locator in self.PASSWORD_FIELDS:

            if self.is_visible(locator, timeout=5):

                logger.info("Password field found. Entering password")

                self.type_text(locator, password)

                self.click_first_available(self.CONTINUE_BUTTONS)

                logger.info("Password submitted successfully")

                return

        logger.info(
            "Password field was not shown. Site may require OTP-based login"
        )

    def enter_mobile_number(self, mobile_number: str) -> None:

        logger.info("Searching for mobile number input field")

        locator = self._first_visible_locator(
            self.MOBILE_NUMBER_INPUTS,
            timeout=10
        )

        logger.info("Mobile number input found using locator: %s", locator)

        element = self.find_first_visible(locator, timeout=10)

        WebDriverWait(
            self.driver,
            settings.explicit_wait
        ).until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        self.driver.execute_script(
            "arguments[0].focus();",
            element
        )

        self.driver.execute_script(
            "arguments[0].value='';",
            element
        )

        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
            element
        )

        element.send_keys(mobile_number)

        logger.info("Mobile number typed into input field")

    def _first_visible_locator(
        self,
        locators: tuple[Locator, ...],
        timeout: int = 5
    ) -> Locator:

        logger.info("Finding first visible locator")

        for locator in locators:

            if self.is_visible(locator, timeout=timeout):

                logger.info("Visible locator found: %s", locator)

                return locator

        logger.error("No visible element found for given locators")

        raise AssertionError(
            f"No visible element was available for locators: {locators}"
        )

    def _type_into_first_available(
        self,
        locators: tuple[Locator, ...],
        text: str
    ) -> None:

        logger.info("Typing text into first available input field")

        for locator in locators:

            if self.is_visible(locator, timeout=5):

                logger.info("Input field found using locator: %s", locator)

                self.type_text(locator, text)

                logger.info("Text entered successfully")

                return

        logger.error("No input field available for given locators")

        raise AssertionError(
            f"No input field was available for locators: {locators}"
        )