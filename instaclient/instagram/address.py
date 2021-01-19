from instaclient import LOGGER
from typing import List, Optional, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient

class Address():
    def __init__(self, address:str, **kwargs):
        try:
            data = json.loads(address)
            self.street_address = data.get('street_address')
            self.zip_code = data.get('zip_code')
            self.city_name = data.get('city_name')
            self.region_name =data.get('region_name')
            self.country_code = data.get('country_code')
            self.exact_city_match = data.get('exact_city_match')
            self.exact_region_match = data.get('exact_region_match')
            self.exact_country_match = data.get('exact_country_match')
        except Exception as error:
            LOGGER.warning('Error when loading location Address', exc_info=error)

    def __repr__(self) -> str:
        return f'Address<{self.city_name}>'