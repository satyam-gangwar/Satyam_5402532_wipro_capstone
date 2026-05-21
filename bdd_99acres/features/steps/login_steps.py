from behave import given, when, then

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

    assert (
        context.otp_completed
        or context.home_page.wait_for_login_overlay_to_close()
    ), (
        "Login popup still open after OTP"
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "login_success"
    )

    logger.info(
        "Login completed successfully"
    )