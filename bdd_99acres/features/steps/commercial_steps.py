from behave import when, then

from pages.home_page import HomePage
from pages.commercial_page import CommercialPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.waits import WaitUtils


logger = LogGen.loggen()

@when("User opens Commercial tab")
def step_open_commercial_tab(context):

    context.home_page = HomePage(
        context.driver
    )

    context.commercial_page = (
        context.home_page.open_commercial_tab()
    )


@when('User searches commercial property for location "{location}"')
def step_search_commercial_property(context, location):

    context.commercial_page.search_commercial_property(
        location
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"commercial_search_results_{location}"
    )

    logger.info(
        f"Commercial property searched for location: {location}"
    )


@when('User selects commercial property type "{property_type}"')
def step_select_property_type(context, property_type):

    context.commercial_page.select_property_type(
        property_type
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"property_type_selected_{property_type}"
    )

    logger.info(
        f"Commercial property type selected: {property_type}"
    )


@then("Commercial results should be loaded")
def step_verify_commercial_results(context):

    assert (
        context.commercial_page.is_results_loaded()
    ), "Commercial results failed to load"

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_results_loaded"
    )

    logger.info(
        "Commercial results loaded successfully"
    )


@then('Commercial results should contain location "{location}"')
def step_verify_results_location(context, location):

    assert (
        context.commercial_page.results_contain_location(
            location
        )
    ), f"Location '{location}' not found in results"

    logger.info(
        f"Commercial results contain location: {location}"
    )


@when('User opens commercial city page for "{city}"')
def step_open_commercial_city_page(context, city):

    context.commercial_page = CommercialPage(
        context.driver
    )

    context.commercial_page.open_commercial_city_page(
        city
    )

    WaitUtils.wait_for_page_load(
        context.driver
    )

    context.commercial_page.wait_for_city_content(
        city
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"commercial_city_page_{city}"
    )

    logger.info(
        f"Commercial city page opened for: {city}"
    )


@when("User scrolls to View Number button")
def step_scroll_to_view_number(context):

    context.commercial_page.scroll_to_contact_button()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "view_number_button_visible"
    )

    logger.info(
        "Scrolled to View Number button"
    )


@when("User clicks View Number button")
def step_click_view_number(context):

    context.commercial_page.click_view_number_button()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "view_number_clicked"
    )

    logger.info(
        "View Number button clicked"
    )


@then("Login popup should be displayed on commercial page")
def step_verify_login_popup(context):

    assert (
        context.commercial_page.verify_login_popup_displayed()
    ), "Login/OTP popup was not displayed"

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_login_popup_displayed"
    )

    logger.info(
        "Login popup displayed successfully"
    )


@then("Invalid commercial search should be handled")
def step_verify_invalid_search(context):

    assert (
        context.commercial_page.is_invalid_search_handled()
    ), "Invalid commercial search was not handled properly"

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "invalid_commercial_search_handled"
    )

    logger.info(
        "Invalid commercial search handled successfully"
    )


@when('User opens invalid commercial URL "{invalid_url}"')
def step_open_invalid_commercial_url(context, invalid_url):

    context.driver.get(
        invalid_url
    )

    WaitUtils.wait_for_page_load(
        context.driver
    )

    context.commercial_page = CommercialPage(
        context.driver
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "invalid_commercial_url_loaded"
    )

    logger.info(
        f"Invalid commercial URL opened: {invalid_url}"
    )