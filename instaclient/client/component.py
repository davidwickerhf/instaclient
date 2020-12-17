from instaclient.client import *

class Component:

    # IG PRIVATE UTILITIES (The client is considered initiated)
    @classmethod
    def __find_element(cls, client:'InstaClient', expectation, url:str=None, wait_time:int=5, retry=True, attempt=0):
        """
        __find_element finds and returns the `WebElement`(s) that match the expectation's XPATH.

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
            wait = WebDriverWait(client.driver, wait_time)
            widgets = wait.until(expectation)
            if widgets == None:
                raise NoSuchElementException()
            else:
                return widgets
        except TimeoutException:
            # Element was not found in time
            logger.debug('INSTACLIENT: Element Not Found...')
            if retry and attempt < 2:
                logger.debug('Retrying find element...')
                if attempt == 0:
                    logger.debug('Checking for cookies/dialogues...')
                    if cls.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.COOKIES_LINK))):
                        cls.__dismiss_cookies()

                    if cls.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.DISMISS_DIALOGUE))):
                        cls.__dismiss_dialogue()
                    return cls.__find_element(expectation, url, wait_time=2, attempt=attempt+1)
                elif retry:
                    logger.debug('Checking if user is logged in...')
                    if ClientUrls.LOGIN_URL in client.driver.current_url:
                        if url is not None:
                            client.driver.get(url)
                            return cls.__find_element(expectation, url, wait_time=2, attempt=attempt+1)
                        else:
                            if client.error_callback:
                                client.error_callback(client.driver)
                            logger.exception('The element with locator {} was not found'.format(expectation.locator))
                            raise NoSuchElementException()
                    elif not client.logged_in:
                        if client.error_callback:
                                client.error_callback(client.driver)
                        raise NotLoggedInError()   
                    else:
                        if client.error_callback:
                            client.error_callback(client.driver)
                        logger.exception('The element with locator {} was not found'.format(expectation.locator))
                        raise NoSuchElementException()
            else:
                if client.error_callback:
                        client.error_callback(client.driver)
                logger.exception('The element with locator {} was not found'.format(expectation.locator))
                raise NoSuchElementException()


    @staticmethod
    def __check_existence(client:'InstaClient', expectation, wait_time:int=2):
        """
        Checks if an element exists.
        Args:
            expectation: EC.class
            wait_time:int: (Seconds) retry window before throwing Exception
        """
        try: 
            wait = WebDriverWait(client.driver, wait_time)
            widgets = wait.until(expectation)
            return True
        except:
            return False


    @classmethod
    def __dismiss_cookies(cls):
        if cls.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.ACCEPT_COOKIES)), wait_time=2.5):
            accept_btn = cls.__find_element(EC.presence_of_element_located((By.XPATH, Paths.ACCEPT_COOKIES)))
            cls.__press_button(accept_btn)
        logger.debug('Dismissed Cookies')


    @classmethod
    def __dismiss_dialogue(cls, wait_time:float=2):
        """
        Dismiss an eventual Instagram dialogue with button text containing either 'Cancel' or 'Not Now'.
        """
        try:
            if cls.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN))):
                dialogue = cls.__find_element(EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN)), wait_time=wait_time)
                cls.__press_button(dialogue)
        except:
            try:
                dialogue = cls.__find_buttons(button_text='Cancel') # TODO add this to translation docs
                cls.__press_button(dialogue)
            except:
                pass


    @classmethod
    def __press_button(cls, button):
        try:
            button.click()
            time.sleep(randrange(0,2))
            cls.__detect_restriction()
            return True
        except:
            x = cls.__find_element(EC.presence_of_element_located((By.XPATH, Paths.X)), wait_time=3)
            x.click()
            time.sleep(1)
            button.click()
            time.sleep(randrange(0,2))
            cls.__detect_restriction()
            return True


    @classmethod
    def __detect_restriction(cls):
        """
        __detect_restriction detects wheter instagram has restricted the current account

        Raises:
            RestrictedAccountError: Raised if the account is restricted
        """
        restriction = cls.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.RESTRICTION_DIALOG)), wait_time=1.2)
        if restriction:
            logger.warn('INSTACLIENT: WARNING: ACCOUNT HAS BEEN RESTRICTED')
            buttons = cls.__find_element(EC.presence_of_element_located((By.XPATH, Paths.RESTRICTION_DIALOGUE_BTNS)), retry=False)
            buttons.click()
            time.sleep(randrange(2,4))
            raise RestrictedAccountError(None)

        block = cls.__check_existence(EC.presence_of_element_located((By.XPATH, Paths.BLOCK_DIV)), wait_time=1.2)
        if block:
            logger.warn('INSTACLIENT: WARNING: ACCOUNT HAS BEEN BLOCKED - Log in Manually')
            raise BlockedAccountError(None)