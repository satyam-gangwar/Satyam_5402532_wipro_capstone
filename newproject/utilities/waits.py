from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WaitUtils:

    @staticmethod
    def wait_for_visibility(driver, locator, timeout=20):
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @staticmethod
    def wait_for_clickable(driver, locator, timeout=20):
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @staticmethod
    def wait_for_presence(driver, locator, timeout=20):
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @staticmethod
    def wait_for_page_load(driver, timeout=30):
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @staticmethod
    def slow_execution(driver, seconds=2):

        try:
            WebDriverWait(driver, seconds).until(
                lambda d: False
            )
        except:
            pass