from selenium.webdriver.support.expected_conditions import presence_of_element_located
from instaclient.client import *

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient

class Component:
    
    def _manage_driver(connect=True, login=True):
        def outer(func):
            @wraps(func)
            def wrapper(self: 'InstaClient', *args, **kwargs):
                LOGGER.debug('INSTACLIENT: Mangage Driver, func: {} | Login: {}'.format(func.__name__, login))
                if connect:
                    if not self.driver:
                        if login and (self.username is None or self.password is None):
                            raise NotLoggedInError()
                        self._connect(login, func=func.__name__)
                    elif login:
                        if not self.logged_in:
                            if (self.username is None or self.password is None):
                                raise NotLoggedInError()
                            else:
                                self._login(self.username, self.password)

                error = False
                result = None
                try:
                    result = func(self, *args, **kwargs)
                    time.sleep(1)
                except Exception as exception:
                    error = exception
                
                time.sleep(randint(1, 2))
                if error:
                    raise error
                else:
                    return result
            return wrapper
        return outer


    def _disconnect(self: 'InstaClient'):
        LOGGER.debug('INSTACLIENT: Discarding driver...')
        if self.driver:
            self.driver.quit()
            self.driver = None
        LOGGER.debug('INSTACLIENT: Driver Discarded')


    def _connect(self: 'InstaClient', login=False, retries=0, func=None):
        LOGGER.debug('INSTACLIENT: Initiating Driver | attempt {} | func: {}'.format(retries, func))
        try:
            if self.driver_type == self.CHROMEDRIVER:
                if self.host_type == self.WEB_SERVER:
                    # Running on web server
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                    mobile_emulation = { "deviceName": "Nexus 5" }
                    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                    chrome_options.add_argument("--window-size=414,896")
                    chrome_options.add_argument("--headless")
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--no-sandbox")
                    chrome_options.add_argument("--disable-setuid-sandbox") 
                    chrome_options.add_argument("--remote-debugging-port=9222")
                    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    chrome_options.add_experimental_option('useAutomationExtension', False)
                    if self.proxy:
                        chrome_options.add_argument('--proxy-server=%s' % self.proxy)
                    self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
                elif self.host_type == self.LOCAHOST:
                    # Running locally
                    chrome_options = webdriver.ChromeOptions()
                    mobile_emulation = { "deviceName": "Nexus 5" }
                    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                    chrome_options.add_argument("--headless") if self.localhost_headless else None
                    chrome_options.add_argument("--disable-dev-shm-usage")
                    chrome_options.add_argument("--no-sandbox")
                    LOGGER.debug('Path: {}'.format(self.driver_path))
                    if self.proxy:
                        chrome_options.add_argument('--proxy-server=%s' % self.proxy)
                    
                    self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)
                else:
                    raise InvaildHostError(self.host_type)
            else:
                raise InvaildDriverError(self.driver_type)
        except WebDriverException as error:
            if retries < 2:
                LOGGER.debug('INSTACLIENT: Error when initiating driver... Trying again')
                self._connect(login=login, retries=retries+1, func='_connect')
            else:
                raise error

        LOGGER.debug(f'Logging in: {login}')
        if login:
            try:
                self._login(self.username, self.password)
            except:
                raise InstaClientError(message='Tried logging in when initiating driver, but username and password are not defined.')


    # IG PRIVATE UTILITIES (The client is considered initiated)
    
    def _find_element(self:'InstaClient', expectation, url:str=None, wait_time:int=5, retry=True, attempt=0):
        """
        _find_element finds and returns the `WebElement`(s) that match the expectation's XPATH.

        If a TimeoutException is raised by the driver, this method will take care of finding the reason of the exception and it will call itcls another time. If the second attemt fails as well, then the `NoSuchElementException` will be raised.

        Args:
            client (InstaClient): InstaClient instance to operate on.
            expectation (expected_conditions class): Any class defined in ``selenium.webdriver.support.expected_conditions``
            url (str): The url where the element is expected to be present
            wait_time (int, optional): Time to wait to find the element. Defaults to 15.
            attempt (int, optional): Number of attempts. IMPORTANT: don't change this attribute's value. Defaults to 0.

        Raises:
            NoSuchElementException: Raised if the element is not found after two attempts.

        Returns:
            WebElement: web element that matches the `expectation` xpath
        """
        try:
            wait = WebDriverWait(self.driver, wait_time)
            widgets = wait.until(expectation)
            if widgets == None:
                raise NoSuchElementException()
            else:
                return widgets
        except TimeoutException:
            # Element was not found in time
            LOGGER.debug('INSTACLIENT: Element Not Found...')
            if retry and attempt < 2:
                LOGGER.debug('Retrying find element...')
                if attempt == 0:
                    LOGGER.debug('Checking for cookies/dialogues...')
                    self._dismiss_useapp_bar()

                    self._dismiss_cookies()

                    self._dismiss_dialogue()
                    return self._find_element(expectation, url, wait_time=2, attempt=attempt+1)
                elif retry:
                    LOGGER.debug('Checking if user is logged in...')
                    if ClientUrls.LOGIN_URL in self.driver.current_url:
                        if url is not None:
                            self.driver.get(url)
                            return self._find_element(expectation, url, wait_time=2, attempt=attempt+1)
                        else:
                            if self.error_callback:
                                self.error_callback(self.driver)
                            LOGGER.exception('The element with locator {} was not found'.format(expectation.locator))
                            raise NoSuchElementException()
                    elif not self.logged_in:
                        if self.error_callback:
                                self.error_callback(self.driver)
                        raise NotLoggedInError()   
                    else:
                        if self.error_callback:
                            self.error_callback(self.driver)
                        LOGGER.exception('The element with locator {} was not found'.format(expectation.locator))
                        raise NoSuchElementException()
            else:
                if self.error_callback:
                        self.error_callback(self.driver)
                LOGGER.exception('The element with locator {} was not found'.format(expectation.locator))
                raise NoSuchElementException()


    def _check_existence(self:'InstaClient', expectation, wait_time:int=2):
        """
        Checks if an element exists.
        Args:
            expectation: EC.class
            wait_time:int: (Seconds) retry window before throwing Exception
        """
        try: 
            wait = WebDriverWait(self.driver, wait_time)
            widgets = wait.until(expectation)
            return True
        except:
            return False


    def _dismiss_cookies(self):
        if self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.ACCEPT_COOKIES)), wait_time=2.5):
            accept_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.ACCEPT_COOKIES)))
            self._press_button(accept_btn)
        LOGGER.debug('Dismissed Cookies')

    
    def _dismiss_useapp_bar(self):
        dismiss_bar = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.USE_APP_BAR)))
        if dismiss_bar:
            dismiss = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.USE_APP_BAR)))
            self._press_button(dismiss)

    
    def _dismiss_dialogue(self, wait_time:float=2):
        """
        Dismiss an eventual Instagram dialogue with button text containing either 'Cancel' or 'Not Now'.
        """
        try:
            if self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN))):
                dialogue = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN)), wait_time=wait_time)
                self._press_button(dialogue)
        except:
            try:
                dialogue = self.__find_buttons(button_text='Cancel') # TODO add this to translation docs
                self._press_button(dialogue)
            except:
                pass


    
    def _press_button(self, button):
        try:
            button.click()
            time.sleep(randrange(0,2))
            self._detect_restriction()
            return True
        except:
            x = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.X)), wait_time=3)
            x.click()
            time.sleep(1)
            button.click()
            time.sleep(randrange(0,2))
            self._detect_restriction()
            return True


    
    def _detect_restriction(self):
        """
        _detect_restriction detects wheter instagram has restricted the current account

        Raises:
            RestrictedAccountError: Raised if the account is restricted
        """
        restriction = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.RESTRICTION_DIALOG)), wait_time=1.2)
        if restriction:
            LOGGER.warn('INSTACLIENT: WARNING: ACCOUNT HAS BEEN RESTRICTED')
            buttons = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.RESTRICTION_DIALOGUE_BTNS)), retry=False)
            buttons.click()
            time.sleep(randrange(2,4))
            raise RestrictedAccountError(None)

        block = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.BLOCK_DIV)), wait_time=1.2)
        if block:
            LOGGER.warn('INSTACLIENT: WARNING: ACCOUNT HAS BEEN BLOCKED - Log in Manually')
            raise BlockedAccountError(None)