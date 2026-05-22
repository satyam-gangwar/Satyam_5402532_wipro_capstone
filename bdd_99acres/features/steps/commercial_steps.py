from behave import given, when, then

from pages.home_page import HomePage
from pages.commercial_page import CommercialPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.waits import WaitUtils
from selenium.webdriver.support.ui import WebDriverWait


logger = LogGen.loggen()


@when("User opens Commercial tab")
def step_open_commercial_tab(context):

    context.home_page = HomePage(context.driver)

    context.commercial_page = (
        context.home_page.open_commercial_tab()
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_tab_opened"
    )

    logger.info("Commercial tab opened successfully")


@given('User opens commercial property page for "{city}"')
def step_open_commercial_city_page(context, city):

    context.commercial_page = CommercialPage(context.driver)

    context.commercial_page.open_commercial_city_page(city)

    WaitUtils.wait_for_page_load(context.driver)

    context.commercial_page.wait_for_city_content(city)

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"commercial_city_page_{city}"
    )

    logger.info(
        f"Commercial property page opened for city: {city}"
    )


@when('User opens commercial city page for "{city}"')
def step_open_commercial_city_page_when(context, city):

    context.commercial_page = CommercialPage(context.driver)

    context.commercial_page.open_commercial_city_page(city)

    WaitUtils.wait_for_page_load(context.driver)

    context.commercial_page.wait_for_city_content(city)

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"commercial_city_page_{city}"
    )

    logger.info(
        f"Commercial city page opened for: {city}"
    )


@when('User enters commercial property location "{location}"')
def step_enter_commercial_location(context, location):

    context.commercial_page.enter_commercial_location(location)

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"commercial_location_entered_{location}"
    )

    logger.info(
        f"Commercial location entered: {location}"
    )


@when("User selects commercial location suggestion")
def step_select_commercial_location_suggestion(context):

    context.commercial_page.select_location_suggestion()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_location_suggestion_selected"
    )

    logger.info(
        "Commercial location suggestion selected"
    )


@when("User clicks Commercial Search button")
def step_click_commercial_search_button(context):

    context.commercial_page.click_search_button()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_search_button_clicked"
    )

    logger.info(
        "Commercial search button clicked"
    )


@when('User searches commercial property for location "{location}"')
def step_search_commercial_property(context, location):

    context.commercial_page.search_commercial_property(location)

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"commercial_search_results_{location}"
    )

    logger.info(
        f"Commercial property searched for location: {location}"
    )


@when('User selects commercial property type "{property_type}"')
def step_select_property_type(context, property_type):

    context.commercial_page.select_property_type(property_type)

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"property_type_selected_{property_type}"
    )

    logger.info(
        f"Commercial property type selected: {property_type}"
    )


@when("User applies Noida commercial filters")
def step_apply_noida_commercial_filters(context):

    context.commercial_page.apply_noida_filters()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "noida_commercial_filters_applied"
    )

    logger.info(
        "Noida commercial filters applied successfully"
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


@when('User opens invalid commercial URL "{invalid_url}"')
def step_open_invalid_commercial_url(context, invalid_url):

    context.driver.get(invalid_url)

    WaitUtils.wait_for_page_load(context.driver)

    context.commercial_page = CommercialPage(context.driver)

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "invalid_commercial_url_loaded"
    )

    logger.info(
        f"Invalid commercial URL opened: {invalid_url}"
    )


@then("User should be redirected to commercial results page")
def step_verify_commercial_results_page(context):

    redirected = context.commercial_page.wait_for_results_page()

    assert redirected, (
        "User was not redirected to commercial results page"
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_results_page_opened"
    )

    logger.info(
        f"Redirected URL: {context.driver.current_url}"
    )


@then("Commercial results should be loaded")
def step_verify_commercial_results_loaded(context):

    assert context.commercial_page.is_results_loaded(), (
        "Commercial results failed to load"
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_results_loaded"
    )

    logger.info(
        "Commercial results loaded successfully"
    )


@then("Commercial result should be loaded")
def step_verify_commercial_result_loaded(context):

    assert context.commercial_page.is_results_loaded(), (
        "Commercial results failed to load"
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_result_loaded"
    )

    logger.info(
        "Commercial result loaded successfully"
    )


@then('Commercial results should contain location "{location}"')
def step_verify_results_location(context, location):

    assert context.commercial_page.results_contain_location(location), (
        f"Location '{location}' not found in results"
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        f"commercial_results_contain_{location}"
    )

    logger.info(
        f"Commercial results contain location: {location}"
    )


@then("Login popup should be displayed on commercial page")
def step_verify_login_popup(context):

    assert context.commercial_page.verify_login_popup_displayed(), (
        "Login/OTP popup was not displayed"
    )

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "commercial_login_popup_displayed"
    )

    logger.info(
        "Login popup displayed successfully"
    )


@then("Invalid commercial search should be handled")
def step_verify_invalid_search(context):

    assert context.commercial_page.is_invalid_search_handled()

@when("User clicks any commercial property from results")
def step_click_any_commercial_property(context):

    context.commercial_page.click_any_property_from_results()


@then("Commercial property detail page should be opened")
def step_verify_property_detail_page(context):

    context.commercial_page.switch_to_latest_tab()

    assert context.commercial_page.is_property_detail_page_opened()
    assert context.commercial_page.is_property_detail_page_opened()

@when("User clicks M3M commercial property")
def step_click_m3m_property(context):

    context.commercial_page.click_fixed_property_m3m()



@when('User fills owner enquiry form with name "{name}"')
def step_fill_owner_form(context, name):

    context.commercial_page.fill_owner_enquiry_form(name)


@then("Owner details form should be filled")
def step_verify_owner_form_filled(context):

    assert context.commercial_page.is_owner_details_form_filled()

    ScreenshotUtil.capture_screenshot(
        context.driver,
        "owner_details_form_verified"
    )

    logger.info("Owner details form filled verified")

    # KEEP PAGE OPEN FOR 10 SECONDS
    try:
        WebDriverWait(context.driver, 10).until(
            lambda driver: False
        )
    except:
        pass


PROPERTY_URL = (
    "https://www.99acres.com/"
    "showroom-for-sale-in-m3m-the-line-sector-72-noida-1640-sqft-spid-V89447334"
)


@when("User opens fixed M3M commercial property detail page")
def step_open_fixed_property(context):

    context.commercial_page = CommercialPage(
        context.driver
    )

    context.driver.get(PROPERTY_URL)

