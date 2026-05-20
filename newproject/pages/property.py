

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PropertyPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)

    def click_fixed_property(self):

        old_url = self.driver.current_url
        old_windows = self.driver.window_handles
        main_window = self.driver.current_window_handle

        property_locator = (
            By.XPATH,
            "//a[contains(.,'Ivory County')]"
        )

        property_element = self.wait.until(
            EC.element_to_be_clickable(property_locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            property_element
        )

        self.driver.execute_script(
            "arguments[0].click();",
            property_element
        )

        self.wait.until(
            lambda d:
            len(d.window_handles) > len(old_windows)
            or d.current_url != old_url
        )

        if len(self.driver.window_handles) > len(old_windows):
            for window in self.driver.window_handles:
                if window != main_window:
                    self.driver.switch_to.window(window)
                    break

        self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )

    def verify_property_page_opened(self):
        return "99acres" in self.driver.current_url.lower()







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

    def open_ivory_county_page(self):

        self.driver.get(
            "https://www.99acres.com/ivory-county-sector-115-noida-npxid-r400436"
        )

        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        self.close_disclaimer_if_present()

    def close_disclaimer_if_present(self):

        try:
            ok_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.OK_GOT_IT)
            )

            ok_button.click()

        except:
            pass

    def fill_brochure_form(self, name):

        name_field = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,'Name') "
                    "or contains(@name,'name')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            name_field
        )

        name_field.clear()
        name_field.send_keys(name)

        entered_name = name_field.get_attribute("value")

        assert entered_name == name

        print("Name entered successfully:", entered_name)

    def click_download_brochure_button(self):

        brochure_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Download Brochure']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            brochure_button
        )

        self.driver.execute_script(
            "arguments[0].click();",
            brochure_button
        )

        print("Clicked on Download Brochure button")