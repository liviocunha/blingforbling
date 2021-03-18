import unittest
from Bling import HookDataProduct


class TestHookChangeInventory(unittest.TestCase):
    def setUp(self):
        data_post = """data={"retorno":{"estoques":[{"estoque":{"codigo":"10001PT37",
        "nome":"Produto Teste Sapato Preto 37","estoqueAtual":7,"depositos":[{"deposito":{"id":"11701636921",
        "nome":"Geral","saldo":"9.0000000000","desconsiderar":"N","saldoVirtual":"9.0000000000"}}]}}]}}"""
        request_body: bytes = bytes(data_post, encoding="raw_unicode_escape")
        self.data = HookDataProduct(request_body)

    def test_request_body_is_bytes(self):
        self.assertIsInstance(self.data.data_bytes, bytes)

    def test_data_is_dict(self):
        self.assertIsInstance(self.data.data_json, dict)

    def test_get_sku_code(self):
        self.assertEqual(self.data.sku, '10001PT37')

    def test_get_current_inventory(self):
        self.assertEqual(self.data.current_inventory, 7)

    def test_get_on_hand_balance(self):
        self.assertEqual(self.data.balance, 9)

    def test_get_reservation_sold(self):
        self.assertEqual(self.data.reservation, 2)


class TestSyncStock(unittest.TestCase):
    def setUp(self):
        obj1 = {'quantity': 3}
        product_update = Obj1(obj1)
        obj2 = {'current_inventory': 2}
        data = Obj2(obj2)
        self.sync_stock = SyncStock(product_update, data)

    def test_diff_quantity(self):
        self.assertEqual(self.sync_stock.diff, -1)

    def test_after_inventory_balance(self):
        self.assertEqual(self.sync_stock.after_stock, 2)

    def test_before_inventory_balance(self):
        self.assertEqual(self.sync_stock.before_stock, 3)


class Obj1(object):
    def __init__(self, obj_dict):
        self.obj_dict = obj_dict
        self.quantity = self._get_quantity()

    def _get_quantity(self):
        return self.obj_dict['quantity']


class Obj2(object):
    def __init__(self, obj_dict):
        self.obj_dict = obj_dict
        self.current_inventory = self._get_current_inventory()

    def _get_current_inventory(self):
        return self.obj_dict['current_inventory']


if __name__ == '__main__':
    unittest.main()
