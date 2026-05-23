from selenium.webdriver.common.by import By


class LoginLocators:

    LOGIN_DIALOG = (
        By.XPATH,
        "//*[contains(., 'Login') "
        "or contains(., 'LOGIN / REGISTER') "
        "or contains(., 'Mobile') "
        "or contains(., 'Email')]"
        "[self::div or self::section or self::form]"
    )

    SESSION_EXPIRED_MESSAGE = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Your session has been expired') "
        "or contains(normalize-space(), 'session has been expired') "
        "or contains(normalize-space(), 'try again later')]"
    )

    MOBILE_NUMBER_INPUTS = (
        (By.XPATH, "//input[@data-for='phnNumber']"),
        (By.XPATH, "//input[@placeholder='Phone Number']"),
        (By.XPATH, "//input[@title='Phone Number']"),
        (By.XPATH, "//input[@type='tel' or contains(@placeholder, 'Phone')]"),
    )

    CONTINUE_BUTTONS = (
        (By.XPATH, "//button[normalize-space()='Continue']"),
        (By.XPATH, "//button[contains(.,'Continue')]"),
        (By.XPATH, "//span[contains(.,'Continue')]"),
    )

    OTP_SCREEN = (
        By.XPATH,
        "//*[contains(text(),'OTP') "
        "or contains(text(),'Enter OTP') "
        "or contains(text(),'Verification')]"
    )