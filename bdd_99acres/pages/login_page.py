'''import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from locators.login_locators import LoginLocators
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.waits import WaitUtils
from selenium.webdriver.support import expected_conditions as EC


logger = LogGen.loggen()


class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    def open_login_popup(self):

        logger.info("Opening Login Popup")

        WaitUtils.wait_for_element_clickable(
            self.driver,
            LoginLocators.LOGIN_ICON
        ).click()

        WaitUtils.wait_for_element_clickable(
            self.driver,
            LoginLocators.LOGIN_OPTION
        ).click()

        logger.info("Login Popup Opened Successfully")

    def enter_mobile_number(self, mobile_number):

        logger.info(
            f"Entering Mobile Number : {mobile_number}"
        )

        element = WaitUtils.wait_for_element_visible(
            self.driver,
            LoginLocators.MOBILE_NUMBER_INPUT
        )

        element.click()
        element.clear()

        self.driver.execute_script(
            "arguments[0].value = '';",
            element
        )

        element.send_keys(mobile_number)

        logger.info("Mobile Number Entered Successfully")

    def click_continue_button(self):

        logger.info("Clicking Continue Button")

        WaitUtils.wait_for_element_clickable(
            self.driver,
            LoginLocators.CONTINUE_BUTTON
        ).click()

        logger.info("Continue Button Clicked Successfully")

    def wait_for_otp_verification(self, seconds=30):

        logger.info(
            f"Waiting {seconds} seconds for OTP verification"
        )

        WebDriverWait(self.driver, seconds).until(
            lambda driver:
            "99acres" in driver.title.lower()
            or "my99acres" in driver.current_url.lower()
            or "user" in driver.page_source.lower()
        )

    def start_mobile_login_and_pause_for_otp(
            self,
            mobile_number,
            otp_pause_seconds=30
    ):

        self.enter_mobile_number(
            mobile_number
        )

        if self.verify_session_expired():
            logger.info(
                "Session expired detected before continue click"
            )

            self.driver.refresh()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "body")
                )
            )

            raise Exception(
                "Session expired before continue click"
            )

        self.click_continue_button()

        if self.verify_session_expired():
            logger.info(
                "Session expired detected after continue click"
            )

            self.driver.refresh()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "body")
                )
            )

            raise Exception(
                "Session expired after continue click"
            )

        logger.info(
            f"Waiting {otp_pause_seconds} seconds for OTP verification"
        )

        WebDriverWait(self.driver, otp_pause_seconds).until(
            lambda driver:
            "99acres" in driver.title.lower()
            or "dashboard" in driver.current_url.lower()
        )

    def verify_session_expired(self):

        logger.info("Checking Session Expired Message")

        try:
            WaitUtils.wait_for_element_visible(
                self.driver,
                LoginLocators.SESSION_EXPIRED_MESSAGE,
                timeout=5
            )

            logger.error("Session Expired Message Displayed")

            return True

        except Exception:
            logger.info("Session Expired Message Not Displayed")

            return False

    def verify_login_successful(self):

        logger.info("Verifying Login Success")

        ScreenshotUtil.capture_screenshot(
            self.driver,
            "login_success"
        )

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Login Success Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        return "99acres" in self.driver.title.lower()'''