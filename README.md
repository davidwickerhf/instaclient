# instaclient

**instaclient** is a Python library for accessing Instagram's features.
With this library you can create Instagram Bots with ease and simplicity. The InstaClient takes advantage of the selenium library to excecute tasks which are not allowed in the Instagram Graph API (such as sending DMs).

The only thing you need to worry about is to spread your requests throughout the day to avoid reaching Instagram spam limits.
> Disclaimer: Please note that this is a research project. I am by no means responsible for any usage of this tool. Use it on your behalf. I'm also not responsible if your accounts get banned due to the extensive use of this tool.

## Current Features
- Follow a user
- Unfollow a user
- Search posts by tag
- Like a users latest posts (max 15 for now)
- Send DMs to a user
- Get a users image media

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install instaclient
```
To update the package:
```bash
pip install -U instaclient
```

## Usage
```python
from instaclient import InstaClient

client = Instaclient(username='username', password='password', driver=InstaClient.CHROMEDRIVER)
# Onlye ChromeDriver is available at the moment
client.login() # Go through Login Procedure
client.send_dm('username', 'Message to send') # send a DM to a user
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update [tests](https://github.com/wickerdevs/instaclient/tree/master/tests) as appropriate.

## Help Community
You can join this [Telegram Group](https://t.me/instaclient) to ask questions about the instabot's functionalities or to contribute to the package!

## Credits
[AUTHORS](https://github.com/wickerdevs/instaclient/blob/master/AUTHORS.rst)

## License
[MIT](https://choosealicense.com/licenses/mit/)


