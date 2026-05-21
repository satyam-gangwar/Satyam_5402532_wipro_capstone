from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from utilities.logger import get_logger


logger = get_logger("PropertyPage")


class PropertyPage:

    DOWNLOAD_BROCHURE_BUTTON = (
        By.XPATH,
        "//*[normalize-space()='Download Brochure']"
    )

    BROCHURE_FORM = (
        By.XPATH,
        "//*[contains(text(),'Download Brochure') "
        "or contains(text(),'Brochure') "
        "or contains(text(),'Enter Mobile') "
        "or contains(text(),'Mobile Number') "
        "or contains(@placeholder,'Mobile') "
        "or contains(@placeholder,'Name') "
        "or contains(@placeholder,'Email')]"
    )

    OK_GOT_IT = (
        By.XPATH,
        "//*[normalize-space()='OK, Got it']"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        self.logger = logger
        self.logger.info("PropertyPage initialized")

    def click_fixed_property(self):

        self.logger.info("Trying to open fixed property: Ivory County")

        old_windows = self.driver.window_handles

        property_locator = (
            By.XPATH,
            "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz'), 'ivory county')]"
        )

        for attempt in range(5):
            try:
                self.logger.info(
                    f"Finding property link attempt: {attempt + 1}"
                )

                property_link = self.wait.until(
                    EC.presence_of_element_located(property_locator)
                )

                href = property_link.get_attribute("href")

                if href:
                    self.logger.info(f"Property URL found: {href}")

                    self.driver.execute_script(
                        "window.open(arguments[0], '_blank');",
                        href
                    )

                    self.wait.until(
                        lambda d: len(d.window_handles) > len(old_windows)
                    )

                    new_window = [
                        window for window in self.driver.window_handles
                        if window not in old_windows
                    ][0]

                    self.driver.switch_to.window(new_window)

                    self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

                    self.logger.info(
                        "Property child page opened successfully"
                    )
                    return

            except StaleElementReferenceException:
                self.logger.warning("Stale element found. Retrying...")
                continue

        raise Exception("Unable to open Ivory County property page")

    def verify_property_page_opened(self):

        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        current_url = self.driver.current_url.lower()
        page_title = self.driver.title.lower()
        page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()

        result = (
            "ivory-county" in current_url
            or "ivory county" in page_title
            or "ivory county" in page_text
        )

        self.logger.info(
            f"Property page verification result: {result}"
        )

        return result

    def open_ivory_county_page(self):

        self.logger.info("Opening Ivory County property page")

        self.driver.get(
            "https://www.99acres.com/ivory-county-sector-115-noida-npxid-r400436"
        )

        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        self.logger.info("Ivory County page loaded successfully")

        self.close_disclaimer_if_present()

    def close_disclaimer_if_present(self):

        self.logger.info("Checking disclaimer popup")

        try:
            ok_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.OK_GOT_IT)
            )

            ok_button.click()

            self.logger.info("Disclaimer popup closed")

        except Exception:
            self.logger.info("Disclaimer popup was not shown")

    def click_download_brochure_button(self):

        self.logger.info("Trying to click Download Brochure button")

        brochure_button = self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BROCHURE_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            brochure_button
        )

        brochure_button = self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BROCHURE_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            brochure_button
        )

        self.logger.info("Clicked on Download Brochure button")

    def fill_brochure_form(self, name):

        self.logger.info("Trying to fill brochure form")

        name_field = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,'Name') "
                    "or contains(@placeholder,'name') "
                    "or contains(@name,'name') "
                    "or contains(@id,'name')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            name_field
        )

        name_field = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,'Name') "
                    "or contains(@placeholder,'name') "
                    "or contains(@name,'name') "
                    "or contains(@id,'name')]"
                )
            )
        )

        name_field.click()
        name_field.clear()

        self.driver.execute_script(
            "arguments[0].value = '';",
            name_field
        )

        name_field.send_keys(name)

        entered_name = name_field.get_attribute("value")

        assert entered_name == name, (
            f"Name not entered. Actual value: {entered_name}"
        )

        self.logger.info("Verified entered name successfully")