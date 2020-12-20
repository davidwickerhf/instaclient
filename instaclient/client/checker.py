from instaclient.client import *
from instaclient.client.component import Component

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient


class Checker(Component):

    # INSTAGRAM FUNCTIONS
    # LOGIN PROCEDURE
    @Component._manage_driver(login=False)
    def _check_status(self: 'InstaClient', _discard_driver:bool=False):
        """
        Check if account is currently logged in. Returns True if account is logged in. Sets the `instaclient.logged_in` variable accordingly.
        Returns False if the driver is not open yet - even if the Instagram credentials (`username` and `password`) are correct.

        Returns:
            bool: True if client is logged in, False if client is not connected or webdriver is not open.
        """
        LOGGER.debug('INSTACLIENT: Check Status')
        if not self.driver:
            return False
        LOGGER.debug(self.driver.current_url)
        if ClientUrls.HOME_URL not in self.driver.current_url:
            self.driver.get(ClientUrls.HOME_URL)
        if self._check_existence( EC.presence_of_element_located((By.XPATH, Paths.COOKIES_LINK))):
            self._dismiss_cookies()
        if self._check_existence( EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN))):
            btn = self._check_existence( EC.presence_of_element_located((By.XPATH, Paths.NOT_NOW_BTN)))
            self._press_button(btn)
            LOGGER.debug('INSTACLIENT: Dismissed dialogue')

        icon = self._check_existence( EC.presence_of_element_located((By.XPATH, Paths.NAV_BAR)), wait_time=4)
        if icon:
            self.logged_in = True
            result = True
        else:
            self.logged_in = False
            result = False
        return result

    """ def is_valid(user):
        pass

    def is_private(user):
        pass """


    @Component._manage_driver(login=False)
    def _is_valid_user(self:'InstaClient', user:str, nav_to_user:bool=True, _discard_driver:bool=False):
        """
        _is_valid_user Checks if a given username is a valid Instagram user.

        Args:
            user (str): Instagram username to check
            nav_to_user (bool, optional): Whether the driver shouldnavigate to the user page or not. Defaults to True.
            _discard_driver (bool, optional): Whether the driver should be closed after the method finishes. Defaults to False.

        Raises:
            NotLoggedInError: Raised if you are not logged into any account
            InvalidUserError: Raised if the user is invalid
            PrivateAccountError: Raised if the user is a private account

        Returns:
            bool: True if the user is valid
        """
        LOGGER.debug('INSTACLIENT: Checking user vadility')
        if nav_to_user:
            self.driver.get(ClientUrls.NAV_USER.format(user))

        if self.driver.current_url != ClientUrls.NAV_USER.format(user):
            self.driver.get(ClientUrls.NAV_USER.format(user))

        LOGGER.debug('INSTACLIENT: Url: {}'.format(self.driver.current_url))
        if self.driver.current_url == ClientUrls.LOGIN_THEN_USER.format(user):
            raise NotLoggedInError()
        elif self.driver.current_url != ClientUrls.NAV_USER.format(user):
            time.sleep(1)
            self.driver.get(ClientUrls.NAV_USER.format(user))
            time.sleep(1)


        if self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.COOKIES_LINK))):
            self._dismiss_cookies()

        element = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)), wait_time=3)
        if element:
            # User does not exist
            LOGGER.debug('INSTACLIENT: {} does not exist.'.format(user))
            raise InvalidUserError(username=user)
        else: 
            LOGGER.debug('INSTACLIENT: {} is a valid user.'.format(user))
            # Operation Successful
            paccount_alert = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.PRIVATE_ACCOUNT_ALERT)))
            if paccount_alert:
                # navigate back to home page
                raise PrivateAccountError(user)
            else:
                return True

