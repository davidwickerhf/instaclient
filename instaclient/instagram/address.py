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

    
    def to_dict(self) -> dict:
        data = vars(self)
        for key in data:
            if isinstance(data[key], list):
                values = list()
                for item in data[key]:
                    if hasattr(item, 'to_dict'):
                        values.append(item.to_dict())
                        continue
                    values.append(item)
                data[key] = values
        return data