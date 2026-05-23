from utils.screenshot_util import ScreenshotUtil
from utils.logger import LogGen
from behave import given, when, then



logger = LogGen.loggen()


@when('User searches commercial property for a location "{location}"')
def step_search_invalid_commercial_location(
    context,
    location
):

    context.commercial_page.enter_commercial_location(
        location
    )

    context.commercial_page.click_search_button()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"invalid_commercial_location_{location}"
    )

    logger.info(
        f"Invalid commercial location searched: {location}"
    )


@then("Invalid commercial search should be a handled")
def step_verify_invalid_commercial_search(context):

    assert (
        context.commercial_page.is_invalid_search_handled()
    ), "Invalid commercial search was not handled"

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "invalid_commercial_search_handled"
    )

    logger.info(
        "Invalid commercial search handled successfully"
    )