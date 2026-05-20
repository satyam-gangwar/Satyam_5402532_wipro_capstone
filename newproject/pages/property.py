

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        logger.info("PropertyPage initialized")

    def click_fixed_property(self):

        logger.info("Trying to open fixed property: Ivory County")

        old_url = self.driver.current_url

        old_windows = self.driver.window_handles

        main_window = self.driver.current_window_handle

        property_locator = (
            By.XPATH,
            "//a[contains(.,'Ivory County')]"
        )

        logger.info("Waiting for property element to become clickable")

        property_element = self.wait.until(
            EC.element_to_be_clickable(property_locator)
        )

        logger.info("Property element found")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            property_element
        )

        logger.info("Scrolled to property element")

        self.driver.execute_script(
            "arguments[0].click();",
            property_element
        )

        logger.info("Clicked on Ivory County property")

        self.wait.until(
            lambda d:
            len(d.window_handles) > len(old_windows)
            or d.current_url != old_url
        )

        logger.info("Detected page navigation or child window opening")

        if len(self.driver.window_handles) > len(old_windows):

            logger.info("Switching to child window")

            for window in self.driver.window_handles:

                if window != main_window:

                    self.driver.switch_to.window(window)

                    logger.info("Switched to child window successfully")

                    break

        self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )

        logger.info("Property page body loaded successfully")

    def verify_property_page_opened(self):

        logger.info("Verifying property page opened")

        result = "99acres" in self.driver.current_url.lower()

        if result:
            logger.info("Property page opened successfully")
        else:
            logger.error("Property page verification failed")

        return result

    def open_ivory_county_page(self):

        logger.info("Opening Ivory County property page")

        self.driver.get(
            "https://www.99acres.com/ivory-county-sector-115-noida-npxid-r400436"
        )

        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        logger.info("Ivory County page loaded successfully")

        self.close_disclaimer_if_present()

    def close_disclaimer_if_present(self):

        logger.info("Checking disclaimer popup")

        try:

            ok_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.OK_GOT_IT)
            )

            ok_button.click()

            logger.info("Disclaimer popup closed")

        except Exception:

            logger.info("Disclaimer popup was not shown")

    def fill_brochure_form(self, name):

        logger.info("Trying to fill brochure form")

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

        logger.info("Name field located successfully")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            name_field
        )

        logger.info("Scrolled to name input field")

        name_field.click()

        logger.info("Clicked name input field")

        name_field.clear()

        logger.info("Cleared existing name field value")

        name_field.send_keys(name)

        logger.info("Entered name into brochure form: %s", name)

        entered_name = name_field.get_attribute("value")

        assert entered_name == name, (
            f"Name not entered. Actual value: {entered_name}"
        )

        logger.info("Verified entered name successfully")

    def click_download_brochure_button(self):

        logger.info("Trying to click Download Brochure button")

        brochure_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Download Brochure']"
                )
            )
        )

        logger.info("Download Brochure button found")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            brochure_button
        )

        logger.info("Scrolled to Download Brochure button")

        self.driver.execute_script(
            "arguments[0].click();",
            brochure_button
        )

        logger.info("Clicked on Download Brochure button")