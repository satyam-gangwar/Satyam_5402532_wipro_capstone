from behave import given, when, then
from selenium.webdriver.support.wait import WebDriverWait

from pages.home_page import HomePage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil


logger = LogGen.loggen()


@given("User launches 99acres application")
def step_launch_99acres(context):

    context.home_page = HomePage(
        context.driver
    )

    context.driver.get(
        context.base_url
    )

    context.home_page.handle_popup()

    logger.info(
        "99acres application launched"
    )


@when("User clicks on Login button")
def step_click_login(context):

    context.home_page.click_login()

    logger.info(
        "Clicked on login button"
    )


@when("User enters valid mobile number from test data")
def step_enter_mobile(context):

    mobile = context.test_data["mobile"]

    context.home_page.enter_mobile_number(
        mobile
    )

    logger.info(
        f"Entered mobile number : {mobile}"
    )


@when("User clicks Continue button")
def step_click_continue(context):

    context.home_page.click_continue()

    logger.info(
        "Clicked continue button"
    )


@when("User submits valid mobile number for OTP")
def step_submit_mobile_for_otp(context):

    mobile = context.mobile_number

    context.home_page.click_login()

    context.home_page.enter_mobile_number(
        mobile
    )

    context.home_page.click_continue()

    if context.home_page.is_session_expired_message_displayed():

        logger.info(
            "Retrying after session expiration"
        )

        context.driver.refresh()

        context.home_page.click_login()

        context.home_page.enter_mobile_number(
            mobile
        )

        context.home_page.click_continue()

    logger.info(
        "Submitted mobile number for OTP"
    )

@when("User enters OTP manually")
def step_manual_otp(context):

    context.otp_completed = (
        context.home_page.wait_for_manual_otp_entry()
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "manual_otp_entry"
    )

    logger.info(
        "Manual OTP entry completed"
    )


@then("Login mobile number field should be displayed")
def step_verify_mobile_field(context):

    assert (
        context.home_page.is_mobile_field_displayed()
    ), "Mobile number field not displayed"

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "login_mobile_field"
    )

    logger.info(
        "Mobile number field verified"
    )


@then("OTP screen should be displayed")
def step_verify_otp_screen(context):

    assert (
        context.home_page.wait_for_otp_screen()
    ), "OTP screen not displayed"

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "otp_screen"
    )

    logger.info(
        "OTP screen displayed successfully"
    )

@then("Login flow should continue after manual OTP entry")
def step_verify_login_after_otp(context):

    print("Enter OTP manually within 40 seconds")

    WebDriverWait(context.driver, 40).until(
        lambda driver: (
            "otp" not in driver.page_source.lower()
        )
    )

    context.home_page.handle_session_expired_popup()

    assert True

@when("User open Commercial tab")
def step_open_commercial_tab(context):

    context.commercial_page = (
        context.home_page.open_commercial_tab()
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_tab_opened"
    )

    logger.info(
        "Commercial tab opened successfully"
    )


@when('User enter commercial property location "{location}"')
def step_enter_commercial_property_location(
    context,
    location
):

    context.commercial_page.enter_commercial_location(
        location
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"commercial_location_{location}"
    )

    logger.info(
        f"Commercial location entered: {location}"
    )


@when("User click Commercial Search button")
def step_click_commercial_search_button(context):

    context.commercial_page.click_search_button()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_search_button_clicked"
    )

    logger.info(
        "Commercial search button clicked"
    )


@then("User should be redirected to commercial result page")
def step_verify_commercial_results_page(context):

    assert (
        context.commercial_page.wait_for_results_page()
    ), "Commercial results page not loaded"

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_results_page"
    )

    logger.info(
        "Commercial results page loaded successfully"
    )


@when("User click any commercial property from results")
def step_click_any_commercial_property(context):

    context.commercial_page.click_any_property_from_results()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_property_clicked"
    )

    logger.info(
        "Commercial property clicked successfully"
    )


@then("Commercial property detail page should b opened")
def step_verify_commercial_property_page(context):

    assert (
        context.commercial_page.is_property_detail_page_opened()
    ), "Commercial property detail page not opened"

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_property_detail_page"
    )

    logger.info(
        "Commercial property detail page opened successfully"
    )