from instaclient.errors.common import InstaClientError


class InvalidShortCodeError(InstaClientError):
    """Raised when trying to navigate to a page with an invalid shortcode.

    Args:
        shortcode (str)
    """
    def __init__(self, shortcode):
        self.shortcode = shortcode
        super().__init__(message='Invalid shortcode')

    def __str__(self):
        return f'{self.shortcode} -> {self.message}'