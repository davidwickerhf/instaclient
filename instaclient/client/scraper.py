import json, requests
from instaclient.client.urls import GraphUrls

class Scraper:
    def __init__(self, logger):
        self.logger = logger

    def _scrape_nodes(self, source:str, parser:function, types:list, count:int=None):
        data = json.loads(source)
        nodes = parser(data)
        self.logger.debug('NODE COUNT:\n{}'.format(len(nodes)))

        selected_nodes = []
        for node in nodes:
            if count is not None and len(selected_nodes) >= count:
                break
            else:
                if node.get('__typename') in types:
                    selected_nodes.append(node)
        return selected_nodes
    
    """def __get_url(self, url):
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url """