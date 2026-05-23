from __future__ import annotations
import subprocess
import allure
import pytest
import os
from selenium.common.exceptions import WebDriverException

from config.settings import settings
from utilities.browser_factory import BrowserFactory
from utilities.logger import get_logger
from utilities.screenshot_utils import capture_screenshot
from utilities.test_data_loader import DEFAULT_TEST_DATA_PATH, TestDataLoader


logger = get_logger("pytest")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default=settings.browser, help="Browser: edge or chrome")
    parser.addoption("--base-url", action="store", default=settings.base_url, help="Application base URL")
    parser.addoption("--headless", action="store_true", default=settings.headless, help="Run Chrome in headless mode")
    parser.addoption(
        "--test-data",
        action="store",
        default=str(DEFAULT_TEST_DATA_PATH),
        help="Path to the centralized JSON test data file",
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    return str(pytestconfig.getoption("--base-url"))


@pytest.fixture(scope="session")
def test_data(pytestconfig: pytest.Config) -> dict:
    return TestDataLoader.load(pytestconfig.getoption("--test-data"))


@pytest.fixture(scope="session")
def driver(request: pytest.FixtureRequest):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    logger.info("Starting browser: %s", browser)
    driver_instance = BrowserFactory.create_driver(browser=browser, headless=headless)
    yield driver_instance
    logger.info("Closing browser after complete test session")
    driver_instance.quit()


@pytest.fixture(autouse=True)
def inject_driver(request: pytest.FixtureRequest, driver):
    request.node.driver = driver
    if request.cls:
        request.cls.driver = driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver is not None:
            try:
                screenshot_path = capture_screenshot(driver, item.nodeid)
                logger.error("Test failed. Screenshot saved: %s", screenshot_path)
            except WebDriverException as exc:
                logger.error("Test failed, but screenshot capture was unavailable: %s", exc)
            try:
                allure.attach(driver.current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)
            except WebDriverException as exc:
                logger.error("Current URL attachment was unavailable: %s", exc)

# Allure test
def pytest_sessionfinish(session, exitstatus):

    print("\nGenerating Allure HTML Report...\n")

    # DELETE OLD REPORT + GENERATE NEW REPORT
    subprocess.run(
        "allure generate reports/allure-results "
        "-o reports/allure-reports --clean",
        shell=True
    )

    # OPEN NEW REPORT
    subprocess.Popen(
        "allure open reports/allure-reports",
        shell=True
    )