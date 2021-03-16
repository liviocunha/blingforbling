from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from braces.views import CsrfExemptMixin
from core.models import Bling, Product
from django.utils import timezone
from Bling import Api, ApiError
from django.core.exceptions import ObjectDoesNotExist


class HookInventoryChangeView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        sku = data['retorno']['estoques'][0]['estoque']['codigo']
        estoque_atual = data['retorno']['estoques'][0]['estoque']['estoqueAtual']
        print(f"Produto: {sku} | Estoque Atual: {estoque_atual}")

        return HttpResponse('\n OK! Status Code 200 \n')


def home(request):
    return render(request, 'index.html')


def insert_products(request):
    accounts_blings = Bling.objects.all()
    logging_future = 0

    try:
        for bling in accounts_blings:
            # All products is base
            products_base = Product.objects.filter(bling=bling)

            # Instance class API Wrapper
            api = Api(bling.api_key)
            products_list = api.get_products()

            for product in products_list:

                sku = api.get_product(product['codigo'])
                try:
                    if sku['estrutura']:
                        # Kit Product
                        logging_future += 1
                except KeyError:
                    try:
                        sku_codigo = str(sku['codigo'])
                        sku_qtd = str(sku['estoqueAtual'])
                        try:
                            product_base = products_base.get(sku=sku_codigo)
                            print(f"Produto {product_base.sku} já está inserido na base.")
                        except ObjectDoesNotExist:
                            Product.objects.create(bling=bling, sku=sku_codigo, quantity=sku_qtd,
                                                   last_update=timezone.now())
                            print(f"Produto: {sku_codigo} | Estoque: {sku_qtd}")
                    except KeyError:
                        # Father Product
                        logging_future += 1
    except ApiError as e:
        print(e.response)
    return render(request, 'index.html')




