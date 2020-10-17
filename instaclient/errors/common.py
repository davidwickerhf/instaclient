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

class InexistingDriverError(InstaClientError):
    """Raised when trying to pass an incorrect driver index in InstaClient.__init__()

    Args:
        driver_int:int: The driver int variable passed to InstaClient()
    """
    def __init__(self, driver_int:int):
        self.driver_int = driver_int
        super().__init__(message='This integer does not refer to any driver')

    def __str__(self):
        return f'{self.driver_int} -> {self.message}'


class IncorrectUsernameError(InstaClientError):
    """Raised when trying to log in with an unexisting account's username
    
    Args:
        username:str: The username that caused the exception
    """
    def __init__(self, username:str):
        self.username = username
        super().__init__(message='The username used to attempt login is not recognized. Check the username.')

    def __str__(self):
        return f'{self.username} -> {self.message}'

class IncorrectPasswordError(InstaClientError):
    """Raised when trying to log in with an incorrect password
    
    Args:
        password:str: The passwod that caused the exception
    """
    def __init__(self, password:str):
        self.password = password
        super().__init__(message='The password used to attempt login is incorrect. Check the password.')

class InexistingUserError(InstaClientError):
    """Raised when searching for an incorrect user's username
    
    Args:
        user:str: The user's username that caused the exception
    """
    def __init__(self, user:str):
        self.user = user
        super().__init__(message='The username was not recognized. Operation to navigate to the user was unsuccessful.')

    def __str__(self):
        return f'{self.user} -> {self.message}'

class InexistingTagError(InstaClientError):
    """Raised when searching for an incorrect tag
    
    Args:
        tag:str: The tag that raised the exception"""
    def __init__(self, tag):
        self.tag = tag
        super().__init__(message='The tag you searched for does not exist.')

    def __str__(self):
        return f'{self.tag} -> {self.message}'
