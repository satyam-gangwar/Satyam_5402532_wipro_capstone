from selenium.webdriver.common.by import By


class HomeLocators:

    POPUP_CLOSE = (
        By.XPATH,
        "//button[normalize-space()='Okay' or normalize-space()='OK']"
    )

    LOGIN_ICON = (
        By.XPATH,
        "//i[contains(@class,'icon_userWhite') "
        "or contains(@class,'user') "
        "or contains(@class,'profile')]"
    )

    LOGIN_BUTTON = (
        By.XPATH,
        "//*[contains(text(),'LOGIN / REGISTER') "
        "or contains(text(),'Login / Register') "
        "or contains(text(),'LOGIN/REGISTER') "
        "or contains(text(),'Login/Register')]"
    )

    MOBILE_NUMBER = (
        By.XPATH,
        "//input[@data-for='phnNumber' "
        "or @placeholder='Phone Number' "
        "or @title='Phone Number' "
        "or @type='tel']"
    )

    CONTINUE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Continue']"
    )

    OTP_INPUT = (
        By.XPATH,
        "//input[@type='tel' or @autocomplete='one-time-code']"
    )

    LOGIN_ADVANTAGES_IMAGE = (
        By.XPATH,
        "//img[contains(@src,'login') or contains(@alt,'login')]"
    )

    MOBILE_ERROR = (
        By.XPATH,
        "//*[contains(text(),'valid mobile') "
        "or contains(text(),'Enter valid') "
        "or contains(text(),'Invalid')]"
    )

    SESSION_EXPIRED_MESSAGE = (
        By.XPATH,
        "//*[contains(normalize-space(), "
        "'Your session has been expired') "
        "or contains(normalize-space(), "
        "'session has been expired')]"
    )


    BUY_TAB = (
        By.XPATH,
        "//a[contains(text(),'Buy')]"
    )

    COMMERCIAL_TAB = (
        By.XPATH,
        "//div[contains(text(),'Commercial')]"
    )



    COMMERCIAL_TAB_SPAN = (
        By.XPATH,
        "//span[contains(text(),'Commercial')]"
    )

    COMMERCIAL_TAB_LINK = (
        By.XPATH,
        "//a[contains(text(),'Commercial')]"
    )

    COMMERCIAL_TAB_GENERIC = (
        By.XPATH,
        "//*[contains(text(),'Commercial')]"
    )

    BUY_TAB_LOCATORS = (
        (
            By.XPATH,
            "//*[normalize-space()='Buy']"
        ),
        (
            By.XPATH,
            "//a[contains(normalize-space(),'Buy')]"
        ),
        (
            By.XPATH,
            "//div[contains(normalize-space(),'Buy')]"
        ),
        (
            By.XPATH,
            "//span[contains(normalize-space(),'Buy')]"
        ),
    )

    COMMERCIAL_TAB_LOCATORS = (
        (
            By.XPATH,
            "//*[normalize-space()='Commercial']"
        ),
        (
            By.XPATH,
            "//a[contains(normalize-space(),'Commercial')]"
        ),
        (
            By.XPATH,
            "//div[contains(normalize-space(),'Commercial')]"
        ),
        (
            By.XPATH,
            "//span[contains(normalize-space(),'Commercial')]"
        ),
    )