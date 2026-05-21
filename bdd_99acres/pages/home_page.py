from locators.home_locators import HomeLocators

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config_reader import ConfigReader
from utils.logger import LogGen
from utils.waits import WaitUtils
from pages.commercial_page import CommercialPage
from selenium.webdriver.common.by import By




logger = LogGen.loggen()


class HomePage:

    def __init__(self, driver):
        self.driver = driver

    def handle_popup(self):
        try:
            popup = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    HomeLocators.POPUP_CLOSE
                )
            )
            self.driver.execute_script(
                "arguments[0].click();",
                popup
            )
            logger.info("Popup closed successfully")

        except TimeoutException:
            logger.info("Popup not present")

        try:
            ActionChains(self.driver).move_by_offset(
                10,
                10
            ).click().perform()

        except Exception:
            logger.info("Page offset click skipped")

    def click_login(self):

        try:
            login_icon = WaitUtils.wait_for_element_visible(
                self.driver,
                HomeLocators.LOGIN_ICON,
                timeout=15
            )

            ActionChains(self.driver).move_to_element(
                login_icon
            ).perform()

            logger.info("Hovered on login icon")

        except Exception:
            logger.info("Login icon hover skipped")

        login_button = WaitUtils.wait_for_element_clickable(
            self.driver,
            HomeLocators.LOGIN_BUTTON,
            timeout=15
        )

        self.driver.execute_script(
            "arguments[0].click();",
            login_button
        )

        logger.info("Login button clicked")

    def enter_mobile_number(self, mobile):
        mobile_field = WaitUtils.wait_for_element_clickable(
            self.driver,
            HomeLocators.MOBILE_NUMBER
        )
        mobile_field.clear()
        mobile_field.send_keys(mobile)
        logger.info("Mobile number entered")

    def click_continue(self):

        continue_button = WaitUtils.wait_for_element_clickable(
            self.driver,
            HomeLocators.CONTINUE_BUTTON
        )

        continue_button.click()

        logger.info("Continue button clicked")

        if self.is_session_expired_message_displayed():
            logger.error(
                "Session expired message displayed"
            )

            self.driver.refresh()

            logger.info(
                "Page refreshed due to session expiration"
            )

            self.click_login()

    def login_with_mobile_until_otp(self, mobile):
        self.click_login()
        self.enter_mobile_number(mobile)
        self.click_continue()
        logger.info("Mobile submitted; waiting for OTP screen")

    def wait_for_otp_screen(self):
        try:
            WaitUtils.wait_for_presence_of_element(
                self.driver,
                HomeLocators.OTP_INPUT,
                timeout=10
            )
            logger.info("OTP screen displayed")
            return True

        except TimeoutException:
            logger.info(
                "OTP input was not detected; login popup may use segmented OTP fields"
            )
            return self.is_mobile_field_displayed()

    def wait_for_manual_otp_entry(self):
        wait_time = ConfigReader.get_manual_otp_wait()

        print(f"Enter OTP manually within {wait_time} seconds")
        logger.info(
            f"Waiting up to {wait_time} seconds for manual OTP entry"
        )

        try:
            WebDriverWait(
                self.driver,
                wait_time,
                ignored_exceptions=(StaleElementReferenceException,)
            ).until(
                lambda driver: not self.is_login_overlay_open()
            )

            logger.info("OTP accepted and login overlay closed")
            return True

        except TimeoutException:
            logger.error("OTP was not completed before wait time ended")
            return False

    def wait_for_login_overlay_to_close(self):
        try:
            WebDriverWait(
                self.driver,
                3,
                ignored_exceptions=(StaleElementReferenceException,)
            ).until(
                lambda driver: not self.is_login_overlay_open()
            )

            logger.info("Login overlay closed after manual OTP entry")
            return True

        except TimeoutException:
            logger.error("Login overlay is still open after manual OTP wait")
            return False

    def is_login_overlay_open(self):
        login_elements = (
            self.driver.find_elements(*HomeLocators.MOBILE_NUMBER)
            + self.driver.find_elements(*HomeLocators.OTP_INPUT)
            + self.driver.find_elements(*HomeLocators.LOGIN_ADVANTAGES_IMAGE)
        )

        try:
            return any(
                element.is_displayed()
                for element in login_elements
            )

        except StaleElementReferenceException:
            logger.info(
                "Login overlay changed while checking display state; retrying wait"
            )
            return True

    def is_mobile_field_displayed(self):
        return len(
            self.driver.find_elements(
                *HomeLocators.MOBILE_NUMBER
            )
        ) > 0

    def get_mobile_validation_message(self):
        messages = self.driver.find_elements(
            *HomeLocators.MOBILE_ERROR
        )

        if messages:
            return messages[0].text

        return ""

    def is_session_expired_message_displayed(self):

        messages = self.driver.find_elements(
            *HomeLocators.SESSION_EXPIRED_MESSAGE
        )

        try:
            return any(
                message.is_displayed()
                for message in messages
            )

        except Exception:
            return False

    def open_buy_tab(self):

        buy_tab = WaitUtils.wait_for_element_clickable(
            self.driver,
            HomeLocators.BUY_TAB,
            timeout=20
        )

        self.driver.execute_script(
            "arguments[0].click();",
            buy_tab
        )

        logger.info(
            "Buy tab opened successfully"
        )

    def open_commercial_tab(self):

        self.open_buy_tab()

        commercial_tab = WaitUtils.wait_for_element_clickable(
            self.driver,
            HomeLocators.COMMERCIAL_TAB,
            timeout=20
        )

        self.driver.execute_script(
            "arguments[0].click();",
            commercial_tab
        )

        logger.info(
            "Commercial tab opened successfully"
        )

        return CommercialPage(
            self.driver
        )