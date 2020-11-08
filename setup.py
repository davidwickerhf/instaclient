from distutils.core import setup
from setuptools import find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'instaclient',         # How you named your package folder (MyLib)
  packages = find_packages(exclude=['tests, drivers']),   # Chose the same as "name"
  version = '1.9.12',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Instagram client built with Python 3.8 and the Selenium package.',  
  long_description=README,
  long_description_content_type="text/markdown",
  author = 'David Wicker',                   # Type in your name
  author_email = 'davidwickerhf@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/wickerdevs/py-instaclient',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/wickerdevs/py-instaclient/archive/v1.9.12.tar.gz',    # I explain this later on
  keywords = ['INSTAGRAM', 'BOT', 'INSTAGRAM BOT', 'INSTAGRAM CLIENT'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'selenium',
          'urllib3',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)