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
# OTHERS
import time, logging, abc, os, threading
from random import randrange, randint
from functools import wraps
from typing import TYPE_CHECKING, Union, Optional, List

# SELENIUM STUFF
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException        
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# INSTACLIENT PACKAGE
from instaclient import LOGGER
from instaclient.client.constants import (ClientUrls, GraphUrls, Paths)
from instaclient.errors import *

from instaclient.instagram import (
    InstaBaseObject,
    Comment,
    Post,
    Profile,
    Hashtag,
    Location,
    Address,
    PostMedia,
    Notification
)
    