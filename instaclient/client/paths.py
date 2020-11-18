class Paths:
    # Login Procedue
    LOGIN_BTN = '//button[@class="sqdOP  L3NKy   y3zKF     "]/div'
    USERNAME_INPUT = '//input[@name="username"]'
    PASSWORD_INPUT = '//input[@name="password"]'
    # Suscpicious Activity Dialogue
    SEND_CODE = '//button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'
    SECURITY_CODE_INPUT = '//input[@name="security_code" or @class="_281Ls zyHYP"]'
    INPUT_CODE_BTN = '//button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'
    INVALID_CODE = '//div[@class="_3_2jD" and @id="form_error"]'
    ERROR_SENDING_CODE = '//div[@class="_3_2jD" and @id="form_error"]//descendant::p'
    RESEND_CODE_BTN = '//p[@class="GusmU  t_gv9    "]//descendant::a'
    SELECT_EMAIL_BTN = '//label[@class="UuB0U " and @for="choice_1"]//descendant::div'
    BACK_BTN = '//svg[@class="_8-yf5 "]'
    SECURITY_CODE_BTN = '//button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'
    # 2FA Verification
    VERIFICATION_CODE = '//input[@name="verificationCode"]'
    VERIFICATION_CODE_BTN = '//button[@class="sqdOP  L3NKy   y3zKF     "]'
    # Pop-Ups
    DISMISS_DIALOGUE = '//button[@class="aOOlW   HoLwm "]'
    # Nav to User Procedure
    INCORRECT_USERNAME_ALERT = '//p[@role="alert" and @id="slfErrorAlert"]'
    INCORRECT_PASSWORD_ALERT = '//div[@class="piCib"]'
    INCORRECT_PASSWORD_ALERT_BTNS = '{}//button[contains(@class, "aOOlW")]'
    ALERT = '//*[@id="slfErrorAlert" or @id="twoFactorErrorAlert"]'
    PAGE_NOT_FOUND = '//h2[@class="_7UhW9      x-6xq    qyrsm KV-D4          uL8Hv     l4b0S    "]'
    PRIVATE_ACCOUNT_ALERT = '//h2[@class="rkEop"]'
    # Send DM Procedure
    DM_TEXT_AREA = '//div[@class="X3a-9"]//descendant::textarea'
    SEND_DM_BTN = '//div[@class="X3a-9"]//descendant::button'
    # Check Login Status Procedure
    NAV_BAR = '//div[@data-testid="mobile-nav-logged-in" and @class="BvyAW"]'
    # ENGAGEMENT PROCEDURES
    # Like Feed Posts
    LIKE_BTN = ''
    # GENERAL
    COOKIES_LINK = '//a[contains(@heref, "cookies") or contains(text(), "Cookie")]'
    ACCEPT_COOKIES = '//button[@class="aOOlW  bIiDR  "]'
    SETTINGS_BTN = '//button[@class="Q46SR"]'
    BUTTON = '//button[text()="{}"]'
    NOT_NOW_BTN = '//button[@class="aOOlW   HoLwm "]'
    RESTRICTION_DIALOG = '//div[@class="_7UhW9   xLCgt      MMzan   _0PwGv         uL8Hv         " and contains(text(), "restrict")]'
    RESTRICTION_DIALOGUE_BTNS = '//div[@class="pbNvD  fPMEg    " and @role="dialog"]//descendant::button'
    BLOCK_DIV = '//div[@class="_7UhW9    vy6Bb     MMzan  KV-D4          uL8Hv     l4b0S    " and contains(text(), "unusual activity")]'
    QUERY_ELEMENT = '//body//descendant::pre'
    # SETTINGS OPTIONS
    LOG_OUT_BTN = '//a[@class="_34G9B H0ovd"]'
    CONFIRM_LOGOUT_BTN = '//button[@class="aOOlW  bIiDR  "]'
    # USER ACCOUNT PROFILE PAGE
    # Followers Procedure
    FOLLOWERS_BTN = '//li[@class=" LH36I"]//descendant::a'
    FOLLOWERS_LIST_MAIN = '//main[@role="main"]'
    FOLLOWERS_LIST = '//ul[@class=" jjbaz _6xe7A"]'
    FOLLOWER_USER_DIV = '{}//li'.format(FOLLOWERS_LIST)
    FOLLOWER_COUNT = '{}//span[@class="g47SY lOXF2"]'.format(FOLLOWERS_BTN)
    # Follow User Procedure
    FOLLOW_BTN = '//button[@class="sqdOP  L3NKy _4pI4F  y3zKF     " or @class="_5f5mN       jIbKX  _6VtSN     yZn4P   "]'
    UNFOLLOW_BTN = '//button[@class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]//descendant::span'
    CONFIRM_UNFOLLOW_BTN = '//button[@class="aOOlW -Cab_   "]'
    REQUESTED_BTN = '//dic[@class=" ffKix "]//descendant::button'
    MESSAGE_USER_BTN = '//button[@class="sqdOP  L3NKy _4pI4F   _8A5w5    "]'
    # USER ACCOUNT DMs PAGE
    DM_LIST_DIV = '//div[@class="N9abW"]//descendant::div'
    DM_USERNAME_DIV = '//div[@class="_7UhW9   xLCgt      MMzan  KV-D4              fDxYl     "]'
