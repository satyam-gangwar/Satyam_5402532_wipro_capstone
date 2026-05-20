
import csv
import time
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.property import PropertyPage
from utilities.logger import get_logger

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

        commercial = home.open_commercial_tab()

        commercial.search_commercial_property(location)

        assert commercial.is_results_loaded()

        property_page = PropertyPage(driver)

        property_page.click_fixed_property()

        assert property_page.verify_property_page_opened()

        logger.info("Fixed property child page opened successfully")

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

        driver.get(
            "https://www.99acres.com/ivory-county-sector-115-noida-npxid-r400436"
        )

        wait = WebDriverWait(driver, 30)

        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        wait.until(
            lambda d: project_name in d.page_source
        )

        assert project_name in driver.page_source

        logger.info(f"Verified text visible: {project_name}")

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

        driver.get(
            "https://www.99acres.com/ivory-county-sector-115-noida-npxid-r400436"
        )

        wait = WebDriverWait(driver, 30)

        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        wait.until(
            lambda d:
            location1 in d.page_source
            and location2 in d.page_source
        )

        assert location1 in driver.page_source
        assert location2 in driver.page_source

        logger.info(f"Verified locations: {location1}, {location2}")

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

        property_page.click_download_brochure_button()

        property_page.fill_brochure_form(
            property_case["name"]
        )

        start_time = time.time()

        WebDriverWait(driver, 12).until(
            lambda d: time.time() - start_time > 10
        )

        logger.info(
            f"Name entered successfully: "
            f"{property_case['name']}"
        )