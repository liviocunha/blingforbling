import unittest
from Bling import HookDataProduct


class TestHookChangeInventory(unittest.TestCase):
    def setUp(self):
        data_post = """data={"retorno":{"estoques":[{"estoque":{"codigo":"10001PT37",
        "nome":"Produto Teste Sapato Preto 37","estoqueAtual":9,"depositos":[{"deposito":{"id":"11701636921",
        "nome":"Geral","saldo":"9.0000000000","desconsiderar":"N","saldoVirtual":"9.0000000000"}}]}}]}}"""
        request_body: bytes = bytes(data_post, encoding="raw_unicode_escape")
        self.data = HookDataProduct(request_body)

    def test_request_body_is_bytes(self):
        self.assertIsInstance(self.data.data_bytes, bytes)

    def test_data_is_dict(self):
        self.assertIsInstance(self.data.data_json, dict)

    def test_get_sku_code(self):
        self.assertEqual(self.data.sku, '10001PT37')


if __name__ == '__main__':
    unittest.main()
