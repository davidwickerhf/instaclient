from instaclient.client import *
from instaclient.client.component import Component

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient


class Checker(Component):

    # INSTAGRAM FUNCTIONS
    # LOGIN PROCEDURE
    @Component._manage_driver(login=False)
    def _check_status(self: 'InstaClient'):
        """
        Check if account is currently logged in. Returns True if account is logged in. Sets the `instaclient.logged_in` variable accordingly.
        Returns False if the driver is not open yet - even if the Instagram credentials (`username` and `password`) are correct.

        Returns:
            bool: True if client is logged in, False if client is not connected or webdriver is not open.
        """
        LOGGER.debug('INSTACLIENT: Check Status')
        return self.logged_in

    """ def is_valid(user):
        pass

    def is_private(user):
        pass """


    @Component._manage_driver(login=False)
    def _is_valid_user(self:'InstaClient', user:str, nav_to_user:bool=True):
        """
        _is_valid_user Checks if a given username is a valid Instagram user.

        Args:
            user (str): Instagram username to check
            nav_to_user (bool, optional): Whether the driver shouldnavigate to the user page or not. Defaults to True.

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


    @Component._manage_driver(login=False)
    def _is_valid_page(self:'InstaClient', url:str=None):
        current = self.driver.current_url
        if url:
            if url != current:
                self.driver.get(url)
                current = self.driver.current_url

        if url and current != url:
            return False

        if self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.PAGE_NOT_FOUND)), wait_time=2):
            return False

        return True
            

        
