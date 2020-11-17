import json

class Scraper:
    def __iterate_nodes(self, source, target_nodes=None, count=None):
        data = json.loads(source)
        nodes = self.__iterate(data, ['node'])
        self.logger.debug('NODES:\n{}'.format(nodes))
        selected_nodes = []
        for node in nodes:
            if node.get('__typename') and node.get('__typename') in target_nodes:
                selected_nodes.append(node)


    def __iterate(self, target_dict:dict, keys:list):
        for i, j in target_dict.items(): 
            if i in keys: 
                yield (i, j) 
            yield from [] if not isinstance(j, dict) else self.__iterate(j, keys) 

    
    """ def __start_request(self):
        url = f'url'
        return scrapy.R
    
    def __parse(self, response):

    
    def __get_url(self, url):
        payload = {'api_key': API_KEY, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url """