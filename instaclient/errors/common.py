#!/usr/bin/env python
#
# Unofficial Instagram Python client. Built with the use of the selenium,
# and requests modules.
# Copyright (C) 2015-2021
# David Henry Francis Wicker <wickerdevs@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains common errors and exceptions raised by the InstaClient"""

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


class InvalidDriverPathError(InstaClientError):
    """Raised when trying to initialize an InstaClient object on a localhost with an unexisting driver Path.

    Args:
        driver_path
    """
    def __init__(self, driver_path):
        self.driver_path = driver_path
        super().__init__(message='No driver was found in the indicated path')

    def __str__(self):
        return f'{self.driver_path} -> {self.message}'



class InvaildHostError(InstaClientError):
    """Raised when trying to pass an incorrect host index in InstaClient.__init__()

    Args:
        host_int:int: The driver int variable passed to InstaClient()
    """
    def __init__(self, host_int:int):
        self.host_int = host_int
        super().__init__(message='This integer does not refer to any host type')

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


class InvalidErrorCallbackError(InstaClientError):
    """Raised when initiating an InstaClient object if the `error_callback` argument is provided but is not a callable object.
    """
    def __init__(self):
        super().__init__(message='The error callback you provided is not a callable.')


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

    
class LoginFloodException(InstaClientError):
    """Raised if a user attempts to log in too many times in a row."""
    def __init__(self):
        super().__init__(message='Please wait a few minutes before trying to log in again.')


class InvaildTagError(InstaClientError):
    """Raised when searching for an incorrect tag
    
    Args:
        tag:str: The tag that raised the exception"""
    def __init__(self, tag):
        self.tag = tag
        super().__init__(message='The tag you searched for does not exist.')

    def __str__(self):
        return f'{self.tag} -> {self.message}'


class InvaildLocationError(InstaClientError):
    """Raised when searching for an incorrect location
    
    Args:
        id (str): ID that caused the error.
        slug (str): Slug that caused the error.
    """
    def __init__(self, id:str, slug:str):
        self.id = id
        self.slug = slug
        super().__init__(message='The tag you searched for does not exist.')

    def __str__(self):
        return f'{self.id} | {self.slug} -> {self.message}'


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


class RestrictedAccountError(InstaClientError):
    """
    Raised when instagram restricts the current account
    """
    def __init__(self, username):
        self.username = username
        super().__init__(message="The account has been restricted by instagram. Use your account normally and wait at least 24 hours before trying again.")

    def __str__(self):
        return f'{self.username} -> {self.message}'


class BlockedAccountError(InstaClientError):
    """
    Raised when instagram restricts the current account
    """
    def __init__(self, username):
        self.username = username
        super().__init__(message="The account has been blocked by instagram. Log into your account manually to unblock it")

    def __str__(self):
        return f'{self.username} -> {self.message}'


class InvalidNotificationTypeError(InstaClientError):
    """ 
    Raised when scraping notifications with an invalid notification type
    """
    def __init__(self, type):
        self.type = type
        super().__init__(message="Trying to scrape notifications with an invalid notification type.")

    def __str__(self):
        return f'{self.type} -> {self.message}'


class InvalidInstaRequestError(InstaClientError):
    """ 
    Raised when scraping a request returns an error
    """
    def __init__(self, request):
        self.request = request
        super().__init__(message="Instagram request failed.")

    def __str__(self):
        return f'{self.request} -> {self.message}'


class InvalidInstaSchemaError(InstaClientError):
    """ 
    Raised when a response json doesn't match the schema
    """
    def __init__(self, func):
        self.func = func
        super().__init__(message="Instagram schema failed.")

    def __str__(self):
        return f'{self.func} -> {self.message}'


class InvalidCursorError(InstaClientError):
    """Raised when an invalid cursor is used to scrape data.
    """
    def __init__(self, cursor):
        self.cursor = cursor
        super().__init__(message='Invalid end cursor')

    def __str__(self):
        return f'{self.message} -> {self.cursor}'