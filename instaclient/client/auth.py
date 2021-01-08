from instaclient.client import *
from instaclient.client.checker import Checker
from instaclient.client.component import Component

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient


class Auth(Checker):
    @Component._manage_driver(login=False)
    def login(self:'InstaClient', username:str, password:str, check_user:bool=True):
        """
        Sign Into Instagram with credentials. Go through 2FA if necessary. Sets the InstaClient variable `InstaClient.logged_in` to True if login was successful.

        Args:
            username (str): The instagram account's username
            password (str): The instagram account's password
            check_user (bool, optional): If False, the username will be considered as valid and will not be checked. If the user is invalid, the login procedure will not be completed. Defaults to True.

        Raises:
            InvalidUserError: Raised if the user is not valid and `check_user` is set to True. Warning: if check_user is set to False and the user is invalid, the login procedure will not be completed.
            InvaildPasswordError: Raised if the password is incorrect.
            SecurityCodeNecessary: Raised if the user's account has 2FA. If this error is raised, you can complete the login procedure with `InstaClient.input_security_code`

        Returns:
            bool: Returns True if login was successful.
        """
        self.username = username
        self.password = password

        # Get Elements
        try:
            # Attempt Login
            self.driver.get(ClientUrls.LOGIN_URL)
            LOGGER.debug('INSTACLIENT: Got Login Page')

            # Detect Cookies Dialogue
            self._dismiss_cookies()

            # Get Form elements
            username_input = self._find_element( EC.presence_of_element_located((By.XPATH,Paths.USERNAME_INPUT)), url=ClientUrls.LOGIN_URL)
            password_input = self._find_element( EC.presence_of_element_located((By.XPATH,Paths.PASSWORD_INPUT)), url=ClientUrls.LOGIN_URL)
            LOGGER.debug('INSTACLIENT: Found elements')
            # Fill out form
            username_input.send_keys(username)
            time.sleep(1)
            password_input.send_keys(password)
            time.sleep(1)
            LOGGER.debug('INSTACLIENT: Filled in form')
            login_btn = self._find_element( EC.presence_of_element_located((By.XPATH,Paths.LOGIN_BTN)), url=ClientUrls.LOGIN_URL)# login button xpath changes after text is entered, find first
            self._press_button(login_btn)
            LOGGER.debug('INSTACLIENT: Sent form')
        except ElementClickInterceptedException as error:
            self.password = None
            self.driver.get(ClientUrls.LOGIN_URL)
            raise InvaildPasswordError(password)
        except Exception as error:
            # User already logged in ?
            result = self.check_status()
            if not result:
                raise error
            else:
                LOGGER.debug('INSTACLIENT: User already logged in?')
                return self.logged_in
        
        # Detect correct Login
        if check_user:
            usernamealert: WebElement = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.INCORRECT_USERNAME_ALERT)), wait_time=3)
            if usernamealert:
                # Username is invalid
                self.driver.get(ClientUrls.LOGIN_URL)
                self.username = None
                raise InvalidUserError(username)

        passwordalert: WebElement = self._check_existence(EC.presence_of_element_located((By.XPATH,Paths.INCORRECT_PASSWORD_ALERT)))
        if passwordalert:
            # Password is incorrect
            self.driver.get(ClientUrls.LOGIN_URL)
            self.password = None
            raise InvaildPasswordError(password)

        # Detect Suspicious Login Attempt Dialogue
        send_code = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.SEND_CODE)))
        if send_code:
            LOGGER.warn('INSTACLIENT: Suspicious Login Attempt.')
            send_code = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_CODE)), wait_time=4)
            self._press_button(send_code)
            LOGGER.warn('INSTACLIENT: Sent Security Code')
            # Detect Error
            alert = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.ERROR_SENDING_CODE)), wait_time=2)
            if alert:
                # Error in sending code, send via email
                email = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SELECT_EMAIL_BTN)), wait_time=4)
                self._press_button(email)
                time.sleep(0.5)
                self._press_button(send_code)
                LOGGER.warn('INSTACLIENT: Sending code via email')
                raise SuspisciousLoginAttemptError(mode=SuspisciousLoginAttemptError.EMAIL)
            raise SuspisciousLoginAttemptError(mode=SuspisciousLoginAttemptError.PHONE)

        # Detect 2FS
        scode_input = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.VERIFICATION_CODE)))
        if scode_input:
            # 2F Auth is enabled, request security code
            LOGGER.warn('INSTACLIENT: 2FA Required. Check Auth App')
            raise VerificationCodeNecessary()

        LOGGER.debug('INSTACLIENT: Credentials are Correct')

        # Discard Driver or complete login
        not_now = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_INFO_BTN)))
        if not_now:
            not_now = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_INFO_BTN)))
            self._press_button(not_now)

        not_now = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN)))
        if not_now:
            not_now = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN)))
            self._press_button(not_now)
        return self.logged_in


    @Component._manage_driver(login=False)
    def resend_security_code(self:'InstaClient'):
        """
        Resend security code if code hasn't been sent successfully. The code is used to verify the login attempt if `instaclient.errors.common.SuspiciousLoginAttemptError` is raised.

        Raises:
            SuspisciousLoginAttemptError: Raised to continue the login procedure. If the `mode` argument of the error is 0, the security code was sent via SMS; if the `mode` argument is 1, then the security code was sent via email.
        Returns:
            bool: True if the code has been sent again successfully. False if an error occured or if the client is no longer on the login page.
        """
        url = self.driver.current_url
        if ClientUrls.SECURITY_CODE_URL in url:
            LOGGER.debug('INSTACLIENT: Resending code')
            resend_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.RESEND_CODE_BTN)), wait_time=4)
            self._press_button(resend_btn)

            alert = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.ERROR_SENDING_CODE)), wait_time=3)
            if alert:
                back_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.BACK_BTN)), wait_time=4)
                self._press_button(back_btn)
                time.sleep(1)
                email = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SELECT_EMAIL_BTN)), wait_time=4)
                self._press_button(email)
                time.sleep(0.5)
                send_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SEND_CODE)), wait_time=4)
                self._press_button(send_btn)
                mode = SuspisciousLoginAttemptError.EMAIL
                raise SuspisciousLoginAttemptError(mode)
            raise SuspisciousLoginAttemptError()
        else:
            LOGGER.warn('Wrong Url when resending code')
            return False


    @Component._manage_driver(login=False)
    def input_security_code(self:'InstaClient', code:int):
        """
        Complete login procedure started with `InstaClient_login()` and insert security code required if `instaclient.errors.common.SuspiciousLoginAttemptError` is raised. Sets `InstaClient.logged_in` attribute to True if login was successful.

        Args:
            code (intorstr): The security code sent by Instagram via SMS or email.

        Raises:
            InvalidSecurityCodeError: Error raised if the code is not valid

        Returns:
            bool: True if login was successful.
        """
        code = str(code)
        if len(code) < 6:
            raise InvalidSecurityCodeError()
        elif not code.isdigit():
            raise InvalidSecurityCodeError()

        scode_input:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SECURITY_CODE_INPUT)), wait_time=4)
        scode_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SECURITY_CODE_BTN)), wait_time=4)
        scode_input.send_keys(code)
        time.sleep(0.5)
        self._press_button(scode_btn)

        # Detect Error
        form_error = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.INVALID_CODE)), wait_time=3)
        if form_error:
            # Invalid Code
            scode_input.clear()
            raise InvalidSecurityCodeError()

        self._dismiss_dialogue()
        return self.logged_in


    @Component._manage_driver(login=False)
    def input_verification_code(self:'InstaClient', code:int):
        """
        Complete login procedure started with `InstaClient_login()` and insert 2FA security code. Sets `instaclient.logged_in` to True if login was successful.

        Args:
            code (int|str): The 2FA security code generated by the Authenticator App or sent via SMS to the user.

        Raises:
            InvalidSecurityCodeError: Raised if the security code is not correct

        Returns:
            bool: Returns True if login was successful
        """
        scode_input: WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.VERIFICATION_CODE)), wait_time=4)
        scode_input.send_keys(code)
        scode_btn: WebElement = self._find_element(EC.element_to_be_clickable((By.XPATH, Paths.VERIFICATION_CODE_BTN)), wait_time=5)
        time.sleep(1)
        self._press_button(scode_btn)

        alert = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.ALERT)))
        if alert:
            # Code is Wrong
            # Clear input field
            scode_input.clear()
            raise InvalidVerificationCodeError()
        else:
            # Auth Correct
            self._dismiss_dialogue()
            return self.logged_in


    @Component._manage_driver(login=False)
    def logout(self:'InstaClient', disconnect:bool=True):
        """
        Check if the client is currently connected to Instagram and logs of the current InstaClient session.

        Returns:
            bool: True if the 
        """
        LOGGER.debug('INSTACLIENT: LOGOUT')
        result = self.check_status()
        username = self.username
        self.username = None
        self.password = None
        if result:
            if disconnect:
                self.disconnect()
                LOGGER.debug('INSTACLIENT: Logged Out')
                return True
            else:
                self.driver.get(ClientUrls.NAV_USER.format(username))
                time.sleep(1)
                settings_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SETTINGS_BTN)), wait_time=4)
                self._press_button(settings_btn)
                logout_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.LOG_OUT_BTN)), wait_time=4)
                self._press_button(logout_btn)
                confirm_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.CONFIRM_LOGOUT_BTN)), wait_time=4)
                self._press_button(confirm_btn)
                LOGGER.debug('INSTACLIENT: Logged Out')
            return True
        else:
            return True

