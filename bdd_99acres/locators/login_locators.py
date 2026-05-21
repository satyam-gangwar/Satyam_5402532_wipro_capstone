from selenium.webdriver.common.by import By


class LoginLocators:

    LOGIN_ICON = (
        By.XPATH,
        "//i[contains(@class,'icon_userWhite') "
        "and contains(@class,'theader__dot')]"
    )

    LOGIN_OPTION = (
        By.XPATH,
        "//*[contains(text(),'LOGIN / REGISTER') "
        "or contains(text(),'Login / Register') "
        "or contains(text(),'LOGIN/REGISTER') "
        "or contains(text(),'Login/Register')]"
    )

    MOBILE_NUMBER_INPUT = (
        By.XPATH,
        "//input[@data-for='phnNumber']"
    )

    CONTINUE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Continue']"
    )

    SESSION_EXPIRED_MESSAGE = (
        By.XPATH,
        "//*[contains(normalize-space(), "
        "'Your session has been expired') "
        "or contains(normalize-space(), "
        "'session has been expired')]"
    )

    LOGIN_DIALOG = (
        By.XPATH,
        "//*[contains(., 'Login') "
        "or contains(., 'LOGIN / REGISTER') "
        "or contains(., 'Mobile') "
        "or contains(., 'Email')]"
        "[self::div or self::section or self::form]"
    )