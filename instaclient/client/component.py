from instaclient.client import *

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient

class Component:

    def _login_required(func):
        @wraps(func)
        def wrapper(self: 'InstaClient', *args, **kwargs):

            if not self.logged_in:
                if (not self.username or not self.password) and not self.session_cookies:
                    raise NotLoggedInError()
                if not self.driver:
                    self.connect(True, func=func.__name__)
                else:
                    self.login(self.username, self.password)

            error = False
            result = None
            try:
                result = func(self, *args, **kwargs)
            except Exception as exception:
                error = exception
            
            time.sleep(randint(1, 2))
            if error:
                raise error
            else:
                return result
        return wrapper


    def _driver_required(func):
        @wraps(func)
        def wrapper(self: 'InstaClient', *args, **kwargs):
            if not self.driver:
                self.connect(func=func.__name__)

            error = False
            result = None
            try:
                result = func(self, *args, **kwargs)
            except Exception as exception:
                error = exception
            
            time.sleep(randint(1, 2))
            if error:
                raise error
            else:
                return result
        return wrapper


    def disconnect(self: 'InstaClient'):
        """Disconnects the client from Instagram

        If ``client.driver`` is not None, the currently connected Web Driver
        will be closed.
        """
        LOGGER.debug('INSTACLIENT: Discarding driver...')
        if self.driver:
            self.driver.quit()
            self.driver = None
        LOGGER.debug('INSTACLIENT: Driver Discarded')


    def connect(self: 'InstaClient', login=False, retries=0, func=None):
        """Connects the client to Instagram

        if ``client.driver`` is None, a new connection will be created
        with the ChromeDriver. This means a new chrome window will be
        opened.

        Args:
            login (bool, optional): If this is set to True, 
                the `instaclient.InstaClient` will try to log in. Defaults to False.

            See the documentation for the ``login()`` method here:
            :meth:`instaclient.InstaClient.login`

            retries (int, optional): Defines the number of times to
                retry connecting to the web driver before raising
                an error. Defaults to 0.
            func (str, optional): The name of the method where the 
                `connect` method is called. This is used for debugging
                purposes and is usually passed automatically by the decorators
                :meth:`instaclient.InstaClient._driver_required` and
                :meth:`instaclient.InstaClient._login_required`. Defaults to None.

        Raises:
            InvaildHostError: This is raised if the atrribute `host_type`, 
                passed to the :meth:`instaclient.InstaClient.__init__` method,
                is invalid.
            InvaildDriverError: This is raised if the atrribute `driver_type`, 
                passed to the :meth:`instaclient.InstaClient.__init__` method,
                is invalid.
            WebDriverException: This is raised if an error occures when
                launching the WebDriver and connecting with Selenium.
            InstaClientError: This is raised if an error occures when trying to
                log in - if the `login` attribute is set to be True.
        """
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
                    chrome_options.add_argument('--log-level=3')
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
                    chrome_options.add_argument('--log-level=3')
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
                self.connect(login=login, retries=retries+1, func='_connect')
            else:
                raise error

        self.driver.get(ClientUrls.HOME_URL)
        self._dismiss_cookies()
        LOGGER.debug(f'Logging in: {login}')
        if login:
            try:
                self.login(self.username, self.password)
            except:
                raise InstaClientError(message='Tried logging in when initiating driver, but username and password are not defined.')
        return self


    # IG PRIVATE UTILITIES (The client is considered initiated)
    
    def _find_element(self:'InstaClient', expectation, url:str=None, wait_time:int=5, retry=True, attempt=0):
        """Finds and returns the `WebElement`(s) that match(es) the expectation's XPATH.

        If the element is not found within the span of time defined by the 
        `wait_time` attribute, the method will check if a few conditions are met, 
        in which case it will call itself again if `retry` is set to True

        Args:
            expectation (:class:expected_conditions): Any class 
                defined in ``selenium.webdriver.support.expected_conditions``
            url (str): The url at which the element is expected to be present
            wait_time (int, optional): Time in seconds to wait to find the element. 
                Defaults to 5 seconds.
            attempt (int, optional): Number of failed attempts. 
                Note:
                    Do not insert a custom value for this attribute, leave it to 0.

        Raises:
            NoSuchElementException: Raised if the element is not found after two attempts.

        Returns:
            :class:`WebElement`: web element that matches the `expectation` xpath
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

    
    def _dismiss_useapp_bar(self, wait_time=1.5):
        dismiss_bar = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.USE_APP_BAR)), wait_time=wait_time)
        if dismiss_bar:
            LOGGER.debug('Dismissed Use App Bar')
            dismiss = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.USE_APP_BAR)))
            self._press_button(dismiss)

    
    def _dismiss_dialogue(self:'InstaClient', wait_time:float=1.5):
        """
        Dismiss an eventual Instagram dialogue with button text containing either 'Cancel' or 'Not Now'.
        """
        try:
            if self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.DIALOGUE)), wait_time=wait_time):
                dialogue = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN)), wait_time=wait_time)
                self._press_button(dialogue)
        except:
            pass

    
    def _press_button(self, button):
        try:
            button.click()
            time.sleep(randrange(0,2))
            self._detect_restriction()
            return True
        except Exception as error:
            LOGGER.warning('Error pressing button', exc_info=error)
            return False


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