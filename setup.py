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

from setuptools import find_packages
from distutils.core import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'instaclient',         # How you named your package folder (MyLib)
  packages = find_packages(exclude=['tests, drivers']),   # Chose the same as "name"
  version = '2.9.11',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Instagram client built with Python 3.8 and the Selenium package.',  
  long_description=README,
  long_description_content_type="text/markdown",
  author = 'David Wicker',                   # Type in your name
  author_email = 'davidwickerhf@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/davidwickerhf/instaclient',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/davidwickerhf/instaclient/archive/v2.9.11.tar.gz',    # I explain this later on
  keywords = ['INSTAGRAM', 'BOT', 'INSTAGRAM BOT', 'INSTAGRAM CLIENT'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'selenium',
          'urllib3',
          'requests'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)