class Paths:
    #TODO Traslate texts in German
    ACCEPT_COOKIES = "/html/body/div[2]/div/div/div/div[2]/button[1]"
    LOGIN_BTN = '//*[@id="loginForm"]/div/div[3]/button'
    USERNAME_INPUT = '//*[@id="loginForm"]/div/div[1]/div/label/input'
    PASSWORD_INPUT = '//*[@id="loginForm"]/div/div[2]/div/label/input'
    SECURITY_CODE = '//input[@name="verificationCode"]'
    SECURITY_CODE_BTN = '//button[@class="sqdOP  L3NKy   y3zKF     "]'
    BUTTON = '//button[text()="{}"]'
    NO_NOTIFICATIONS_BTN = '/html/body/div[4]/div/div/div/div[3]/button[2]'

    ALERT = '//*[@id="slfErrorAlert" or @id="twoFactorErrorAlert"]'
    PAGE_NOT_FOUND = '//*[@class="Cv-5h"]'
    PRIVATE_ACCOUNT_ALERT = '//*[@class="rkEop"]'
    FOLLOWER_COUNT = 'g47SY '
    FOLLOWERS_BTN = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
    FOLLOWERS_DIV = '//div[@class="PZuss"]//a'
    FOLLOWER_USER_DIV = '/html/body/div[4]/div/div/div[2]/ul/div/li[%s]'

    DM_TEXT_AREA = '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea'
    SEND_DM_BTN = '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button'