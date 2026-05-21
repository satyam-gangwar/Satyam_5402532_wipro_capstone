from selenium.webdriver.common.by import By


class CommercialLocators:

    SEARCH_INPUT = (
        By.XPATH,
        "//input[contains(@placeholder,'Search') or contains(@type,'text')]"
    )

    RESULTS_CONTAINER = (
        By.XPATH,
        "//*[contains(@class,'srpTuple') "
        "or contains(@class,'tupleCard') "
        "or contains(@class,'listings') "
        "or contains(@class,'results')]"
    )

    CONTACT_BUTTON = (
        By.XPATH,
        "//*[contains(.,'Get Phone') or "
        "contains(.,'Contact') or "
        "contains(.,'Phone') or "
        "contains(.,'View Number')]"
    )

    LOGIN_OTP_POPUP = (
        By.XPATH,
        "//*[contains(.,'Login') or "
        "contains(.,'Mobile') or "
        "contains(.,'OTP') or "
        "contains(.,'Phone')]"
    )

    VERIFIED_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Verified')]"
    )

    BUDGET_MIN = (
        By.XPATH,
        "//*[contains(text(),'No min')]"
    )

    BUDGET_MIN_OPTION = (
        By.XPATH,
        "//*[contains(text(),'10 Lac')]"
    )

    APARTMENT_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Residential Apartment')]"
    )

    VILLA_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Independent House/Villa')]"
    )

    BHK_2 = (
        By.XPATH,
        "//*[contains(text(),'2 BHK')]"
    )

    BHK_3 = (
        By.XPATH,
        "//*[contains(text(),'3 BHK')]"
    )

    READY_TO_MOVE = (
        By.XPATH,
        "//*[contains(text(),'Ready to move')]"
    )

    UNDER_CONSTRUCTION = (
        By.XPATH,
        "//*[contains(text(),'Under Construction')]"
    )

    OWNER = (
        By.XPATH,
        "//*[contains(text(),'Owner')]"
    )

    CENTRAL_NOIDA = (
        By.XPATH,
        "//*[contains(text(),'Central Noida')]"
    )

    SECTOR_150 = (
        By.XPATH,
        "//*[contains(text(),'Sector 150')]"
    )

    RESULT_CARDS = (
        By.XPATH,
        "//*[contains(@class,'srpTuple') "
        "or contains(@class,'tupleCard')]"
    )