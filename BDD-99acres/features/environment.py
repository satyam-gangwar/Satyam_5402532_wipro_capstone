from utils.logger import LogGen
from utils.config_reader import ConfigReader
from utils.screenshot_util import ScreenshotUtil
from utils.csv_reader import CSVReader

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions


logger = LogGen.loggen()


def before_all(context):

    logger.info("Loading test data before execution")

    context.login_data = CSVReader.first_row(
        "test_data/login_data.csv"
    )

    logger.info(
        f"Login test data loaded : {context.login_data}"
    )


def before_scenario(context, scenario):

    logger.info("========================================")
    logger.info(
        f"STARTING SCENARIO : {scenario.name}"
    )

    browser = ConfigReader.get_browser()
    base_url = ConfigReader.get_base_url()
    implicit_wait = ConfigReader.get_implicit_wait()
    headless = ConfigReader.get_headless()

    context.base_url = base_url

    login_data = CSVReader.first_row(
        "test_data/login_data.csv"
    )

    context.test_data = login_data

    context.mobile_number = (
        login_data["mobile_number"]
    )

    context.test_data["mobile"] = (
        login_data["mobile_number"]
    )

    logger.info(
        f"Mobile number loaded from CSV : {context.mobile_number}"
    )

    if browser.lower() == "chrome":

        logger.info("Launching Chrome Browser")

        chrome_options = Options()

        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        if headless:
            chrome_options.add_argument("--headless")

        context.driver = webdriver.Chrome(
            options=chrome_options
        )

    elif browser.lower() == "edge":

        logger.info("Launching Edge Browser")

        edge_options = EdgeOptions()

        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")

        if headless:
            edge_options.add_argument("--headless")

        context.driver = webdriver.Edge(
            options=edge_options
        )

    else:

        logger.error(
            f"Unsupported browser : {browser}"
        )

        logger.info(
            "Defaulting to Edge Browser"
        )

        edge_options = EdgeOptions()

        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_argument("--disable-extensions")

        if headless:
            edge_options.add_argument("--headless")

        context.driver = webdriver.Edge(
            options=edge_options
        )

    context.driver.maximize_window()

    context.driver.implicitly_wait(
        implicit_wait
    )

    context.driver.get(
        base_url
    )

    logger.info(
        "Browser Opened & Maximized Successfully"
    )


def after_scenario(context, scenario):

    logger.info(
        f"Scenario Status : {scenario.status}"
    )

    if (
        scenario.status.name == "failed"
        or scenario.status.name == "error"
    ):

        logger.error(
            f"SCENARIO FAILED : {scenario.name}"
        )

        screenshot_path = (
            ScreenshotUtil.capture_screenshot(
                context.driver,
                scenario.name
            )
        )

        logger.info(
            f"Screenshot Saved : {screenshot_path}"
        )

    else:

        logger.info(
            f"SCENARIO PASSED : {scenario.name}"
        )

    context.driver.quit()

    logger.info(
        "Browser Closed Successfully"
    )

    logger.info(
        "========================================"
    )