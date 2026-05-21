from selenium.webdriver.common.by import By


class CommercialLocators:

    '''
    SEARCH_INPUT = (
        By.XPATH,
        "//input[contains(@placeholder,'Search') "
        "or contains(@placeholder,'City') "
        "or contains(@placeholder,'Locality') "
        "or @type='text']"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//*[contains(@id,'search') "
        "or contains(@class,'search') "
        "or normalize-space()='Search']"
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
    )'''

    SEARCH_BOX_AREA = (
        By.XPATH,
        "//*[contains(text(),'Search') "
        "or contains(text(),'City') "
        "or contains(text(),'Locality')]"
    )

    SEARCH_INPUT = (
        By.XPATH,
        "//input | //*[@contenteditable='true']"
    )

    SEARCH_BUTTON = (
        By.ID,
        "searchform_search_btn"
    )




    RESULTS_CONTAINER = (
        By.XPATH,
        "//*[contains(@class,'srpTuple') "
        "or contains(@class,'tupleCard') "
        "or contains(@class,'tupleCardWrap') "
        "or contains(@class,'listings') "
        "or contains(@class,'results') "
        "or contains(text(),'properties')]"
    )


    SEARCH_SUGGESTION = (
        By.XPATH,
        "(//*[contains(@class,'suggest') "
        "or contains(@id,'suggest')])[1]"
    )



    RESULTS = (
        By.XPATH,
        "//*[contains(@class,'tupleCard') "
        "or contains(@class,'srpTuple') "
        "or contains(text(),'properties')]"
    )

    SHOP_OPTION = (
        By.XPATH,
        "//*[contains(text(),'Shop') "
        "or contains(text(),'Retail')]"
    )

    VIEW_NUMBER_BUTTON = (
        By.XPATH,
        "//*[contains(text(),'View Number') "
        "or contains(text(),'Get Phone') "
        "or contains(text(),'Contact')]"
    )

    LOGIN_POPUP = (
        By.XPATH,
        "//input[@type='tel']"
    )

    LOCATION_SUGGESTION = (
        By.XPATH,
        "(//*[contains(text(),'Mumbai') or contains(@title,'Mumbai')])[1]"
    )

