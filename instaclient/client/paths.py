class Paths:
    #TODO Traslate texts in German
    # Login Procedue
    ACCEPT_COOKIES = "/html/body/div[2]/div/div/div/div[2]/button[1]"
    LOGIN_BTN = '//button[@class="sqdOP  L3NKy   y3zKF     "]/div'
    USERNAME_INPUT = '//input[@name="username"]'
    PASSWORD_INPUT = '//input[@name="password"]'
    SECURITY_CODE = '//input[@name="verificationCode"]'
    SECURITY_CODE_BTN = '//button[@class="sqdOP  L3NKy   y3zKF     "]'
    NO_NOTIFICATIONS_BTN = '/html/body/div[4]/div/div/div/div[3]/button[2]'
    # Nav to User Procedure
    INCORRECT_USERNAME_ALERT = '//p[@role="alert" and @id="slfErrorAlert"]'
    INCORRECT_PASSWORD_ALERT = '//div[@class="piCib"]'
    INCORRECT_PASSWORD_ALERT_BTNS = '{}//button[contains(@class, "aOOlW")]'
    ALERT = '//*[@id="slfErrorAlert" or @id="twoFactorErrorAlert"]'
    PAGE_NOT_FOUND = '//h2[@class="_7UhW9      x-6xq    qyrsm KV-D4          uL8Hv     l4b0S    "]'
    PRIVATE_ACCOUNT_ALERT = '//h2[@class="rkEop"]'
    # Followers Procedure
    FOLLOWERS_BTN = '//li[@class=" LH36I"]//descendant::a'
    FOLLOWERS_LIST_MAIN = '//main[@role="main"]'
    FOLLOWERS_LIST = '//ul[@class=" jjbaz _6xe7A"]'
    FOLLOWER_USER_DIV = '{}//li'.format(FOLLOWERS_LIST)
    FOLLOWER_COUNT = '{}//span[@class="g47SY lOXF2"]'.format(FOLLOWERS_BTN)
    # Send DM Procedure
    DM_TEXT_AREA = '//div[@class="X3a-9"]//descendant::textarea'
    SEND_DM_BTN = '//div[@class="X3a-9"]//descendant::button'
    # Check Login Status Procedure
    NAV_BAR = '//div[@data-testid="mobile-nav-logged-in" and @class="BvyAW"]'
    # GENERAL
    BUTTON = '//button[text()="{}"]'