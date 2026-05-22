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

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[contains(.,'Search')] "
        "| //*[@id='searchform_search_btn']"
    )

    SEARCH_SUGGESTION = (
        By.XPATH,
        "(//*[contains(@class,'suggest') "
        "or contains(@id,'suggest') "
        "or contains(@class,'autocomplete')])[1]"
    )

    LOCATION_SUGGESTION = (
        By.XPATH,
        "(//*[contains(text(),'Mumbai') "
        "or contains(@title,'Mumbai') "
        "or contains(text(),'Noida') "
        "or contains(text(),'Delhi')])[1]"
    )

    LOCATION_SUGGESTION_DYNAMIC = (
        By.XPATH,
        "//*[contains(text(),'{location}') "
        "or contains(@title,'{location}')]"
    )

    SUGGESTION_BOX = (
        By.XPATH,
        "(//*[contains(@class,'suggest') "
        "or contains(@id,'suggest') "
        "or contains(@class,'autocomplete') "
        "or contains(@role,'option')])[1]"
    )

    MUMBAI_SUGGESTION = (
        By.XPATH,
        "//*[contains(text(),'Mumbai') or contains(@title,'Mumbai')]"
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

    RESULTS = (
        By.XPATH,
        "//*[contains(@class,'tupleCard') "
        "or contains(@class,'srpTuple') "
        "or contains(text(),'properties')]"
    )

    RESULTS_TEXT = (
        By.XPATH,
        "//*[contains(text(),'properties') "
        "or contains(text(),'Property') "
        "or contains(text(),'Mumbai') "
        "or contains(text(),'Noida') "
        "or contains(text(),'Delhi')]"
    )

    #RESULT_CARDS = (
       # By.XPATH,
       # "//*[contains(@class,'tuple') "
      #  "or contains(@class,'card') "
     #   "or contains(@class,'srpTuple')]"
    #)

    CITY_TEXT = (
        By.XPATH,
        "//*[contains(.,'{city}')]"
    )

    SHOP_OPTION = (
        By.XPATH,
        "//*[contains(text(),'Shop') "
        "or contains(text(),'Retail') "
        "or contains(text(),'Shops')]"
    )

    VIEW_NUMBER_BUTTON = (
        By.XPATH,
        "//*[contains(text(),'View Number') "
        "or contains(text(),'Get Phone') "
        "or contains(text(),'Contact')]"
    )

    CONTACT_BUTTON = (
        By.XPATH,
        "//button[contains(.,'View Number') "
        "or contains(.,'Contact') "
        "or contains(.,'Get Phone')]"
    )

    LOGIN_POPUP = (
        By.XPATH,
        "//input[@type='tel']"
    )

    LOGIN_OTP_POPUP = (
        By.XPATH,
        "//*[contains(text(),'Login') "
        "or contains(text(),'OTP') "
        "or contains(text(),'Mobile') "
        "or contains(text(),'Phone')]"
    )

    APPLIED_FILTER_CHIPS = (
        By.XPATH,
        "//*[contains(@class,'tag') "
        "or contains(@class,'chip') "
        "or contains(@class,'filter') "
        "or contains(@class,'selected')]"
    )

    OWNER = (
        By.XPATH,
        "//*[contains(normalize-space(),'Owner')]"
    )

    VERIFIED_CHECKBOX = (
        By.XPATH,
        "//*[contains(text(),'Verified')]"
    )

    HEADER_OWNER = (
        By.XPATH,
        "//*[normalize-space()='Owner' "
        "or contains(normalize-space(),'Owner')]"
    )

    HEADER_VERIFIED = (
        By.XPATH,
        "//*[normalize-space()='Verified' "
        "or contains(normalize-space(),'Verified')]"
    )

    HEADER_READY_TO_MOVE = (
        By.XPATH,
        "//*[normalize-space()='Ready To Move' "
        "or normalize-space()='Ready to move' "
        "or contains(normalize-space(),'Ready')]"
    )

    HEADER_WITH_PHOTOS = (
        By.XPATH,
        "//*[normalize-space()='With Photos' "
        "or contains(normalize-space(),'Photos')]"
    )

    BUDGET_NO_MIN = (
        By.XPATH,
        "//*[contains(text(),'No min') "
        "or contains(text(),'Min')]"
    )

    BUDGET_MIN_10_LAC = (
        By.XPATH,
        "//*[contains(text(),'10 Lac') "
        "or contains(text(),'10 Lacs')]"
    )

    BUDGET_NO_MAX = (
        By.XPATH,
        "//*[contains(text(),'No max') "
        "or contains(text(),'Max')]"
    )

    SHOPS_FILTER = (
        By.XPATH,
        "//*[contains(text(),'Shops') "
        "or contains(text(),'Shop') "
        "or contains(text(),'Retail')]"
    )

    SHOWROOM_FILTER = (
        By.XPATH,
        "//*[contains(normalize-space(),'Showroom') "
        "or contains(normalize-space(),'Showrooms')]"
    )

    KIOSK_FILTER = (
        By.XPATH,
        "//*[contains(text(),'Kiosk') "
        "or contains(text(),'Kiosks')]"
    )

    SECURITY_GUARD = (
        By.XPATH,
        "//*[contains(text(),'Security Guard') "
        "or contains(text(),'Security')]"
    )

    SHOPS_RETAIL = (
        By.XPATH,
        "//*[contains(text(),'Shops') "
        "or contains(text(),'Retail')]"
    )

    READY_TO_MOVE_OFFICES = (
        By.XPATH,
        "//*[contains(text(),'Ready to move offices') "
        "or contains(text(),'Ready to move')]"
    )

    BARE_SHELL_OFFICES = (
        By.XPATH,
        "//*[contains(text(),'Bare shell offices') "
        "or contains(text(),'Bare shell')]"
    )

    PRE_LEASED_SPACES = (
        By.XPATH,
        "//*[contains(text(),'Pre-leased Spaces') "
        "or contains(text(),'Pre-leased') "
        "or contains(text(),'Pre leased')]"
    )

    CO_WORKING = (
        By.XPATH,
        "//*[contains(text(),'Co-working') "
        "or contains(text(),'Coworking')]"
    )

    SECTOR_62 = (
        By.XPATH,
        "//*[contains(text(),'Sector 62')]"
    )

    SECTOR_132 = (
        By.XPATH,
        "//*[contains(text(),'Sector 132')]"
    )

    READY_TO_MOVE_COMMERCIAL = (
        By.XPATH,
        "//*[contains(text(),'Ready to move') "
        "or contains(text(),'Ready To Move')]"
    )

    UNDER_CONSTRUCTION_COMMERCIAL = (
        By.XPATH,
        "//*[contains(text(),'Under Construction') "
        "or contains(text(),'Under construction')]"
    )

    RESALE = (
        By.XPATH,
        "//*[contains(text(),'Resale')]"
    )

    NEW_BOOKING = (
        By.XPATH,
        "//*[contains(text(),'New Booking') "
        "or contains(text(),'New booking')]"
    )

    LIFT = (
        By.XPATH,
        "//*[contains(text(),'Lift')]"
    )

    POWER_BACKUP = (
        By.XPATH,
        "//*[contains(text(),'Power Backup') "
        "or contains(text(),'Power backup')]"
    )

    RESULT_CARDS = (
        By.XPATH,
        "//*[contains(@class,'srpTuple') or contains(@class,'tupleCard')]"
    )

    PROPERTY_TITLE_LINK = (
        By.XPATH,
        "(//a[contains(@href,'/property/') "
        "or contains(@href,'spid') "
        "or contains(@href,'commercial')])[1]"
    )

    PROPERTY_CARD_FALLBACK = (
        By.XPATH,
        "(//*[contains(@class,'srpTuple') "
        "or contains(@class,'tupleCard') "
        "or contains(@class,'tupleCardWrap')])[1]"
    )

    FIXED_PROPERTY_ONE_FNG = (
        By.XPATH,
        "//*[contains(normalize-space(),'One FNG by Group 108')]"
    )

    FIXED_PROPERTY_ONE_FNG_FALLBACK = (
        By.XPATH,
        "//*[contains(normalize-space(),'Bare shell Office Space') "
        "and contains(normalize-space(),'Sector 142')]"
    )

    M3M_THE_LINE_PROPERTY = (
        By.XPATH,
        "//*[contains(normalize-space(),'M3M The Line')]"
    )

    M3M_THE_LINE_FALLBACK = (
        By.XPATH,
        "//*[contains(normalize-space(),'Showroom for sale') "
        "and contains(normalize-space(),'Sector 72')]"
    )


    PROPERTY_DETAIL_PAGE = (
        By.XPATH,
        "//*[contains(text(),'Commercial Showrooms for Sale') "
        "or contains(text(),'Showroom for sale') "
        "or contains(text(),'Commercial property')]"
    )

    #CONTACT_OWNER_BUTTON = (
     #   By.ID,
      #  "contactDealerBtn"
    #)
    OWNER_DETAILS_TAB = (
        By.XPATH,
        "//*[contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'owner details') "
        "or contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'view owner') "
        "or contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'contact dealer') "
        "or contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'get phone')]"
    )




    OWNER_FORM_TRIGGER = (
        By.XPATH,
        "//*[@id='contactDealerBtn'] "
        "|//*[contains(@data-label,'CONTACT_DEALER_OWNER')] "
        "|//*[contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'contact owner')] "
        "|//*[contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'view phone')]"
    )

    OWNER_NAME_INPUT = (
        By.XPATH,
        "(//input[@type='text' "
        "or contains(@placeholder,'Name') "
        "or contains(@name,'name') "
        "or contains(@id,'name')])[1]"
    )

    OWNER_MOBILE_INPUT = (
        By.XPATH,
        "(//input[contains(@placeholder,'Mobile') "
        "or contains(@placeholder,'Phone') "
        "or contains(@placeholder,'Number') "
        "or @type='tel'])[last()]"
    )