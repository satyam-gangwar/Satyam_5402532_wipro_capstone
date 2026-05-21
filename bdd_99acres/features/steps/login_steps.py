from behave import given, when, then

from pages.home_page import HomePage


@given("user launches the 99acres application")
def step_open_homepage(context):
    context.home_page = HomePage(context.driver)
    context.home_page.open_home_page(context.base_url)


@when("user opens the login popup")
def step_open_login_popup(context):
    context.home_page.click_login()


@when("user enters valid mobile number")
def step_enter_mobile_number(context):
    context.home_page.enter_mobile_number(context.mobile_number)
    context.home_page.click_continue()


@when("user waits for OTP verification")
def step_wait_for_otp(context):
    assert context.home_page.wait_for_manual_otp_entry()


@then("user should be logged in successfully")
def step_verify_login(context):
    assert context.home_page.verify_login_successful()