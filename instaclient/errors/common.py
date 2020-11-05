"""This module contains common errors and exceptions raised by the InstaClient"""
from selenium.common.exceptions import WebDriverException

class InstaClientError(Exception):
    """Base InstaClient Exception

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class InvaildHostError(InstaClientError):
    """Raised when trying to pass an incorrect host index in InstaClient.__init__()

    Args:
        host_int:int: The driver int variable passed to InstaClient()
    """
    def __init__(self, host_int:int):
        self.host_int = host_int
        super().__init__(message='This integer does not refer to any host')

    def __str__(self):
        return f'{self.host_int} -> {self.message}'


class InvaildDriverError(InstaClientError):
    """Raised when trying to pass an incorrect driver index in InstaClient.__init__()

    Args:
        driver_int:int: The driver int variable passed to InstaClient()
    """
    def __init__(self, driver_int:int):
        self.driver_int = driver_int
        super().__init__(message='This integer does not refer to any driver')

    def __str__(self):
        return f'{self.driver_int} -> {self.message}'


class InvalidUserError(InstaClientError):
    """Raised when searching for an incorrect user's username or when trying to login with an unexisting account's username
    
    Args:
        user:str: The user's username that caused the exception
    """
    def __init__(self, username:str):
        self.username = username
        super().__init__(message='The username was not recognized. Operation to navigate to the user was unsuccessful.')

    def __str__(self):
        return f'{self.username} -> {self.message}'


class InvaildPasswordError(InstaClientError):
    """Raised when trying to log in with an incorrect password
    
    Args:
        password:str: The passwod that caused the exception
    """
    def __init__(self, password:str):
        self.password = password
        super().__init__(message='The password used to attempt login is incorrect. Check the password.')


class VerificationCodeNecessary(InstaClientError):
    """Raised if security code is necessary to log in"""
    def __init__(self):
        super().__init__(message='The 2FA security code is required. The Security Code has been sent to the user\'s phone number or Authenticator App.')


class SuspisciousLoginAttemptError(InstaClientError):
    PHONE = 0
    EMAIL = 1
    """Raised if security code is necessary to log in"""
    def __init__(self, mode=PHONE):
        self.mode = mode
        super().__init__(message='Suspicious Login Attempt warning detected. Sending code mode: '.format(mode))

    def __str__(self):
        return f'{self.message}'


class InvalidSecurityCodeError(InstaClientError):
    """Raised if security code inputted by the user is invalid"""
    def __init__(self):
        super().__init__(message='The used security code is invalid.')


class InvalidVerificationCodeError(InstaClientError):
    """Raised if security code inputted by the user is invalid"""
    def __init__(self):
        super().__init__(message='The used verification code is invalid. Please try entering the code correctly or ask the user to input one of their backup codes')


class InvaildTagError(InstaClientError):
    """Raised when searching for an incorrect tag
    
    Args:
        tag:str: The tag that raised the exception"""
    def __init__(self, tag):
        self.tag = tag
        super().__init__(message='The tag you searched for does not exist.')

    def __str__(self):
        return f'{self.tag} -> {self.message}'


class PrivateAccountError(InstaClientError):
    """Raise when trying to access a private account's followers
    Args: 
        user:str: The username of the private account that caused the error
    """
    def __init__(self, user):
        self.user = user
        super().__init__(message='Getting this account\'s followers is impossible as this account is private')

    def __str__(self):
        return f'{self.user} -> {self.message}'


class FollowRequestSentError(InstaClientError):
    def __init__(self, user):
        self.user = user
        super().__init__(message='A follow request has been sent to this user, but it hasn\'t been accepted yet, hence it is impossible to send a DM.')

    def __str__(self):
        return f'{self.user} -> {self.message}'


class NotLoggedInError(InstaClientError):
    """Raised when trying to use a client method without being logged into instagram"""
    def __init__(self):
        super().__init__(message="InstaClient is not logged in.")
