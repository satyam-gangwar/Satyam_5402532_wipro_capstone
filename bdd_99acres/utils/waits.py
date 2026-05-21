from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.config_reader import ConfigReader
from utils.logger import LogGen


logger = LogGen.loggen()

class WaitUtils:

    timeout_duration = ConfigReader.get_timeout()
    @staticmethod
    def wait_for_element_visible(
            driver,
            locator,
            timeout=timeout_duration
    ):

        try:
            logger.info(
                f"Waiting for element visibility : {locator}"
            )
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(
                f"Element visible successfully : {locator}"
            )
            return element
        except TimeoutException:
            logger.error(
                f"Timeout waiting for visibility : {locator}"
            )
            raise

    @staticmethod
    def wait_for_element_clickable(
            driver,
            locator,
            timeout=timeout_duration
    ):

        try:
            logger.info(
                f"Waiting for element clickable : {locator}"
            )
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            logger.info(
                f"Element clickable successfully : {locator}"
            )
            return element
        except TimeoutException:
            logger.error(
                f"Timeout waiting for clickable : {locator}"
            )
            raise

    @staticmethod
    def wait_for_presence_of_element(
            driver,
            locator,
            timeout=timeout_duration
    ):

        try:
            logger.info(
                f"Waiting for element presence : {locator}"
            )
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            logger.info(
                f"Element present successfully : {locator}"
            )
            return element
        except TimeoutException:
            logger.error(
                f"Timeout waiting for presence : {locator}"
            )
            raise

    @staticmethod
    def wait_for_title_contains(
            driver,
            title,
            timeout=timeout_duration
    ):

        try:
            logger.info(
                f"Waiting for title contains : {title}"
            )
            result = WebDriverWait(driver, timeout).until(
                EC.title_contains(title)
            )
            logger.info(
                f"Title contains successfully : {title}"
            )
            return result
        except TimeoutException:
            logger.error(
                f"Timeout waiting for title : {title}"
            )
            raise

    @staticmethod
    def wait_for_alert(
            driver,
            timeout=timeout_duration
    ):

        try:
            logger.info("Waiting for alert")
            alert = WebDriverWait(driver, timeout).until(
                EC.alert_is_present()
            )
            logger.info("Alert appeared successfully")
            return alert
        except TimeoutException:
            logger.error("Timeout waiting for alert")
            raise

    @staticmethod
    def wait_for_invisibility(
            driver,
            locator,
            timeout=timeout_duration
    ):

        try:
            logger.info(
                f"Waiting for invisibility : {locator}"
            )
            result = WebDriverWait(driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            logger.info(
                f"Element invisible successfully : {locator}"
            )
            return result
        except TimeoutException:
            logger.error(
                f"Timeout waiting for invisibility : {locator}"
            )
            raise