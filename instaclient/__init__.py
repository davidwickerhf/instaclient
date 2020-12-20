from typing import TYPE_CHECKING
import logging


if TYPE_CHECKING:
    from instaclient.client.instaclient import InstaClient
    from instaclient.errors.common  import *
    from instaclient.instagram import *


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)