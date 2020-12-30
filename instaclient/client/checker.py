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
    def _is_valid_user(self:'InstaClient', user:str):
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
        profile:Profile = self._scrape_profile(user)
        if not profile:
            if ClientUrls.LOGIN_URL in self.driver.current_url:
                raise NotLoggedInError()
            raise InvalidUserError(user)
        if profile.is_private:
            raise PrivateAccountError(user)
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
            

        
