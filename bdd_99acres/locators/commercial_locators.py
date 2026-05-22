from selenium.webdriver.common.by import By


class CommercialLocators:






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

    #SEARCH_BUTTON = (
     #   By.ID,
      #  "searchform_search_btn"
    #)
    SEARCH_BUTTON = (
        By.XPATH,
        "//button[contains(.,'Search')]"
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


    CONTACT_BUTTON = (
        By.XPATH,
        "//button[contains(.,'View Number') or contains(.,'Contact')]"
    )

    LOGIN_OTP_POPUP = (
        By.XPATH,
        "//*[contains(text(),'Login') or contains(text(),'OTP') or contains(text(),'Mobile')]"
    )


    RESULT_CARDS = (
        By.XPATH,
        "//*[contains(@class,'tuple') or contains(@class,'card')]"
    )

    CITY_TEXT = (
        By.XPATH,
        "//*[contains(.,'{city}')]"
    )

    RESULTS_TEXT = (
        By.XPATH,
        "//*[contains(text(),'properties') "
        "or contains(text(),'Property') "
        "or contains(text(),'Mumbai') "
        "or contains(text(),'Noida') "
        "or contains(text(),'Delhi')]"
    )

    LOCATION_SUGGESTION_DYNAMIC = (
        By.XPATH,
        "//*[contains(text(),'{location}')]"
    )

    SUGGESTION_BOX = (
        By.XPATH,
        "//*[contains(@class,'suggest') or contains(@id,'suggest')]"
    )

    MUMBAI_SUGGESTION = (
        By.XPATH,
        "//*[contains(text(),'Mumbai')]"
    )

    VERIFIED_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Verified')]"
    )

    # Type of property section






    # Investment Options section
    PRE_LEASED_SPACES = (
        By.XPATH,
        "//div[contains(.,'Investment Options')]//*[contains(.,'Pre-leased Spaces')]"
    )

    CO_WORKING = (
        By.XPATH,
        "//div[contains(.,'Investment Options')]//*[contains(.,'Co-working')]"
    )

    # Localities section
    SECTOR_62 = (
        By.XPATH,
        "//div[contains(.,'Localities')]//*[contains(.,'Sector 62')]"
    )

    SECTOR_132 = (
        By.XPATH,
        "//div[contains(.,'Localities')]//*[contains(.,'Sector 132')]"
    )

    # Construction Status section
    READY_TO_MOVE_COMMERCIAL = (
        By.XPATH,
        "//div[contains(.,'Construction Status')]//*[contains(.,'Ready to move')]"
    )

    UNDER_CONSTRUCTION_COMMERCIAL = (
        By.XPATH,
        "//div[contains(.,'Construction Status')]//*[contains(.,'Under Construction')]"
    )

    # Purchase type section
    RESALE = (
        By.XPATH,
        "//div[contains(.,'Purchase type')]//*[contains(.,'Resale')]"
    )

    NEW_BOOKING = (
        By.XPATH,
        "//div[contains(.,'Purchase type')]//*[contains(.,'New Booking')]"
    )

    # Amenities section
    LIFT = (
        By.XPATH,
        "//div[contains(.,'Amenities')]//*[contains(.,'Lift')]"
    )

    POWER_BACKUP = (
        By.XPATH,
        "//div[contains(.,'Amenities')]//*[contains(.,'Power Backup')]"
    )

    APPLIED_FILTER_CHIPS = (
        By.XPATH,
        "//*[contains(@class,'tag') or contains(@class,'chip') or contains(@class,'filter')]"
    )

    OWNER = (
        By.XPATH,
        "//*[contains(normalize-space(),'Owner')]"
    )

    BUDGET_NO_MIN = (
        By.XPATH,
        "//*[normalize-space()='No min']"
    )
    COWORKING = (
        By.XPATH,
        "//*[contains(text(),'Co-working')]"
    )

    RENTAL_YIELD = (
        By.XPATH,
        "//*[contains(text(),'Rental Yield')]"
    )




    BUDGET_MIN_10_LAC = (
        By.XPATH,
        "//*[contains(text(),'10 Lac')]"
    )

    BUDGET_NO_MAX = (
        By.XPATH,
        "//*[normalize-space()='No max']"
    )



    SECURITY_GUARD = (
        By.XPATH,
        "//*[contains(text(),'Security Guard')]"
    )

    READY_TO_MOVE_OFFICES = (
        By.XPATH,
        "//div[contains(.,'Type of property')]//*[contains(.,'Ready to move offices')]"
    )

    SHOPS_RETAIL = (
        By.XPATH,
        "//div[contains(.,'Type of property')]//*[contains(.,'Shops & Retail')]"
    )

    BARE_SHELL_OFFICES = (
        By.XPATH,
        "//div[contains(.,'Type of property')]//*[contains(.,'Bare shell offices')]"
    )