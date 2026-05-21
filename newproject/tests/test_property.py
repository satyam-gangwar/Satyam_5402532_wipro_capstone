import csv
import time
import pytest
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.property import PropertyPage

from utilities.logger import get_logger
from utilities.screenshot_utils import capture_screenshot


logger = get_logger("property")


def load_property_data():

    data = []

    with open(
        "test_data/property_data.csv",
        newline=""
    ) as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:
            data.append(row)

    return data


class TestPropertyNavigation:

    def attach_screenshot(self, driver, name):

        screenshot_path = capture_screenshot(
            driver,
            name
        )

        allure.attach.file(
            screenshot_path,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

        logger.info(
            "Screenshot captured: %s",
            screenshot_path
        )

    @pytest.mark.parametrize(
        "property_case",
        load_property_data()
    )
    def test_click_property_and_open_child_page(
        self,
        driver,
        base_url,
        property_case
    ):

        location = property_case["location2"]

        home = HomePage(driver)

        home.open(base_url)
        home.wait_for_page_load()

        self.attach_screenshot(
            driver,
            "01_homepage_loaded"
        )

        commercial = home.open_commercial_tab()

        self.attach_screenshot(
            driver,
            "02_commercial_tab_opened"
        )

        commercial.search_commercial_property(location)

        self.attach_screenshot(
            driver,
            "03_commercial_search_results"
        )

        assert commercial.is_results_loaded()

        property_page = PropertyPage(driver)

        property_page.click_fixed_property()

        self.attach_screenshot(
            driver,
            "04_property_child_page_opened"
        )

        assert property_page.verify_property_page_opened()

        logger.info(
            "Fixed property child page opened successfully"
        )

        start_time = time.time()

        WebDriverWait(driver, 35).until(
            lambda d: time.time() - start_time > 30
        )

    @pytest.mark.parametrize(
        "property_case",
        load_property_data()
    )
    def test_ivory_county_title_visible(
            self,
            driver,
            property_case
    ):
        project_name = property_case["project_name"]

        property_page = PropertyPage(driver)

        property_page.open_ivory_county_page()

        self.attach_screenshot(
            driver,
            "01_ivory_county_page_loaded"
        )

        WebDriverWait(driver, 30).until(
            lambda d: project_name in d.page_source
        )

        self.attach_screenshot(
            driver,
            "02_ivory_county_title_visible"
        )

        assert project_name in driver.page_source

        logger.info(
            "Verified text visible: %s",
            project_name
        )

    @pytest.mark.parametrize(
        "property_case",
        load_property_data()
    )

    def test_ivory_county_location_visible(
            self,
            driver,
            property_case
    ):
        location1 = property_case["location1"]

        location2 = property_case["location2"]

        property_page = PropertyPage(driver)

        property_page.open_ivory_county_page()

        wait = WebDriverWait(driver, 30)

        self.attach_screenshot(
            driver,
            "01_location_page_loaded"
        )

        wait.until(
            lambda d:
            location1 in d.page_source
            and location2 in d.page_source
        )

        self.attach_screenshot(
            driver,
            "02_location_visible"
        )

        assert location1 in driver.page_source

        assert location2 in driver.page_source

        logger.info(
            "Verified locations: %s, %s",
            location1,
            location2
        )



    @pytest.mark.parametrize(
        "property_case",
        load_property_data()
    )
    def test_download_brochure_button(
        self,
        driver,
        property_case
    ):

        property_page = PropertyPage(driver)

        property_page.open_ivory_county_page()

        self.attach_screenshot(
            driver,
            "01_ivory_county_page_opened"
        )

        property_page.click_download_brochure_button()

        self.attach_screenshot(
            driver,
            "02_brochure_popup_opened"
        )

        property_page.fill_brochure_form(
            property_case["name"]
        )

        self.attach_screenshot(
            driver,
            "03_name_entered_in_brochure_form"
        )

        start_time = time.time()

        WebDriverWait(driver, 12).until(
            lambda d: time.time() - start_time > 10
        )

        logger.info(
            "Name entered successfully: %s",
            property_case["name"]
        )