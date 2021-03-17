import requests
import json


class Api(object):
    """API Wrapper for Bling ERP."""

    def __init__(self, api_key):
        """
        :param:
        api_key (str): 72 characters of API key provided by Bling
        """

        self.api_key = api_key
        # Article Bling site: https://ajuda.bling.com.br/hc/pt-br/articles/360046937853
        self.root_uri = 'https://bling.com.br/Api/v2'
        self.session = requests.Session()

    def _requests(self, method, uri, params=None, data=None):
        # Article Bling site: https://ajuda.bling.com.br/hc/pt-br/articles/360046422714
        url = f"{self.root_uri}{uri}/json/?apikey={self.api_key}"
        try:
            resp = self.session.request(method, url, data=data, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            raise ApiError(e.request, e.response)
        except requests.exceptions.RequestException as e:
            raise ApiError(e.request)

    def _get_items(self, resource, element, params=None):
        elements = []
        page = 1

        while True:
            try:
                uri = f"/{resource}/page={page}"
                resp = self._requests('GET', uri, params=params)
                items = resp['retorno'][resource]
                for item in items:
                    elements.append(item[element])
                page += 1
            except KeyError:
                break
        return elements

    def get_products(self, type=None, situation=None):
        filters = []
        params = {}

        if type:
            one_filter = f"tipo[{type}]"
            filters.append(one_filter)

        if situation:
            one_filter = f"situacao[{situation}]"
            filters.append(one_filter)

        if len(filters):
            filters_value = ';'.join(filters)
            params = {'filters': filters_value}

        return self._get_items('produtos', 'produto', params)

    def get_product(self, sku):
        uri = f"/produto/{sku}"
        params = {'estoque': 'S'}
        resp = self._requests('GET', uri, params=params)
        return resp['retorno']['produtos'][0]['produto']

    def update_product(self):
        pass

    def update_stock(self):
        pass


class ApiError(Exception):
    def __init__(self, request, response=None):
        self.request = request
        self.response = response


class HookDataProduct(object):
    """
    If the "Send batch data" parameter is disabled in Bling the callback sends only 1 product at a time
    and this Class receives this post and deals with the necessary fields to use in updating the stock.
    """
    def __init__(self, request_body):
        """
        :param:
        data_bytes (bytes): POST callback change inventory
        data_json (dict): Dictionary with the product data structure
        sku (string): Code of product
        current_inventory (int): Current inventory of product
        balance (int): Balance of product
        reservation (int): Reservation of product
        """

        self.data_bytes = request_body
        self.data_json = self._json_loads()
        self.sku = self._get_sku_code()

    @staticmethod
    def _to_string(data_bytes):
        data_str = data_bytes.decode("UTF-8")
        return data_str[5:]

    def _json_loads(self):
        data_str = self._to_string(self.data_bytes)
        return json.loads(data_str)

    def _get_sku_code(self):
        return self.data_json['retorno']['estoques'][0]['estoque']['codigo']

