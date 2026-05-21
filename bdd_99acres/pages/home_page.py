import allure

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.login_locators import LoginLocators
from utils.config_reader import ConfigReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.waits import WaitUtils


logger = LogGen.loggen()


class HomePage:

    def __init__(self, driver):
        self.driver = driver

    def open_home_page(self, url):
        logger.info(f"Opening URL : {url}")

        self.driver.get(url)
        self.driver.maximize_window()

        ScreenshotUtil.capture_screenshot(
            self.driver,
            "home_page_opened"
        )

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Home Page",
            attachment_type=allure.attachment_type.PNG
        )

    def click_login(self):
        logger.info("Opening Login Popup")

        login_icon = WaitUtils.wait_for_element_visible(
            self.driver,
            LoginLocators.LOGIN_ICON
        )

        ActionChains(self.driver).move_to_element(
            login_icon
        ).perform()

        WaitUtils.wait_for_element_clickable(
            self.driver,
            LoginLocators.LOGIN_OPTION
        ).click()

        logger.info("Login popup opened")

    def enter_mobile_number(self, mobile):
        logger.info(f"Entering mobile number: {mobile}")

        mobile_field = WaitUtils.wait_for_element_clickable(
            self.driver,
            LoginLocators.MOBILE_NUMBER_INPUT
        )

        mobile_field.click()
        mobile_field.clear()

        self.driver.execute_script(
            "arguments[0].value = '';",
            mobile_field
        )

        mobile_field.send_keys(mobile)

        logger.info("Mobile number entered")

    def click_continue(self):
        WaitUtils.wait_for_element_clickable(
            self.driver,
            LoginLocators.CONTINUE_BUTTON
        ).click()

        logger.info("Continue button clicked")

    def login_with_mobile_until_otp(self, mobile):
        self.click_login()
        self.enter_mobile_number(mobile)
        self.click_continue()

        logger.info("Mobile submitted; waiting for OTP screen")

    def wait_for_manual_otp_entry(self):
        wait_time = ConfigReader.get_manual_otp_wait()

        print(f"Enter OTP manually within {wait_time} seconds")

        logger.info(
            f"Waiting up to {wait_time} seconds for manual OTP entry"
        )

        try:
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: not self.is_login_overlay_open()
            )

            logger.info("OTP accepted and login overlay closed")

            return True

        except TimeoutException:
            logger.error("OTP was not completed before wait time ended")

            return False

    def is_login_overlay_open(self):
        login_elements = (
            self.driver.find_elements(*LoginLocators.MOBILE_NUMBER_INPUT)
            + self.driver.find_elements(*LoginLocators.LOGIN_DIALOG)
        )

        return any(
            element.is_displayed()
            for element in login_elements
        )

    def verify_login_successful(self):
        ScreenshotUtil.capture_screenshot(
            self.driver,
            "login_success"
        )

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="Login Success Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        return "99acres" in self.driver.title.lower()