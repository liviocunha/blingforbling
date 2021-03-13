import requests


class Api(object):
    """API Wrapper for Bling ERP."""

    def __init__(self, api_key):
        """
        :param:
        api_key (str): 72 characters of API key provided by Bling
        """

        self.api_key = api_key
        # Article Bling site: https://ajuda.bling.com.br/hc/pt-br/articles/360046937853
        self.root_uri = 'https//bling.com.br/Api/V2'
        self.session = requests.Session()

    def get_products(self):
        pass

    def get_product(self):
        pass

    def update_product(self):
        pass

    def update_stock(self):
        pass

