import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)

from instaclient.client.instaclient import InstaClient
from instaclient.errors.common  import *
from instaclient.instagram import *


