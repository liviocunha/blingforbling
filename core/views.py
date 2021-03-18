import json
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from braces.views import CsrfExemptMixin
from core.models import AccountBling, Product, Movement
from django.utils import timezone
from Bling import Api, ApiError, HookDataProduct, SyncStock
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


class HookInventoryChangeView1(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = HookDataProduct(request.body)

        bling1 = AccountBling.objects.get(id=1)
        products_base = Product.objects.filter(bling=bling1)
        product_update = products_base.get(sku=data.sku)

        sync_stock = SyncStock(product_update, data)

        if sync_stock.diff != 0:
            print()
            print(timezone.now())
            print(f"SKU: {product_update.sku} | Conta: {bling1.name} | Diferença: {sync_stock.diff} | Anterior: {sync_stock.before_stock}"
                  f" | Novo: {sync_stock.after_stock}")
            product_update.last_update = timezone.now()
            product_update.quantity = data.current_inventory
            product_update.save(update_fields=['last_update', 'quantity'])

            Movement.objects.create(quantity=sync_stock.diff, product=product_update,
                                    after_stock=sync_stock.after_stock, before_stock=sync_stock.before_stock,
                                    time=timezone.now(), bling=bling1, updated=False)
            bling2 = AccountBling.objects.get(id=2)
            blings_updated = sync_other_account(bling2)
            print()
            print(timezone.now())
            print(f"Produto atualizado: {blings_updated}")
            print()
        return HttpResponse('\n OK! Status Code 200 \n')


class HookInventoryChangeView2(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = HookDataProduct(request.body)

        bling2 = AccountBling.objects.get(id=2)
        products_base = Product.objects.filter(bling=bling2)
        product_update = products_base.get(sku=data.sku)

        sync_stock = SyncStock(product_update, data)

        if sync_stock.diff != 0:
            print()
            print(timezone.now())
            print(f"SKU: {product_update.sku} | Conta: {bling2.name} | Diferença: {sync_stock.diff} | Anterior: {sync_stock.before_stock}"
                  f" | Novo: {sync_stock.after_stock}")
            product_update.last_update = timezone.now()
            product_update.quantity = data.current_inventory
            product_update.save(update_fields=['last_update', 'quantity'])

            Movement.objects.create(quantity=sync_stock.diff, product=product_update,
                                    after_stock=sync_stock.after_stock, before_stock=sync_stock.before_stock,
                                    time=timezone.now(), bling=bling2, updated=False)
            bling1 = AccountBling.objects.get(id=1)
            blings_updated = sync_other_account(bling1)
            print()
            print(timezone.now())
            print(f"Produto atualizado: {blings_updated}")
            print()
        return HttpResponse('\n OK! Status Code 200 \n')


def sync_other_account(bling):
    list_sku = []
    try:
        movement_products = Movement.objects.filter(updated=False)
        list_movement = list(movement_products)
        for movement in list_movement:
            products_data = Product.objects.filter(sku=movement.product.sku)
            product = products_data.get(bling=bling)
            if product.bling != movement.bling:
                new_quantity = product.quantity + movement.quantity
                product.quantity = new_quantity
                product.last_update = timezone.now()
                product.save(update_fields=['quantity', 'last_update'])
                movement.updated = True
                movement.save(update_fields=['updated'])
                try:
                    api = Api(bling.api_key)
                    update = api.update_stock(code=product.sku, qty=new_quantity)
                    list_sku.append(f"UPDATED BLING: {bling.name} | SKU: {product.sku} | QTD: {new_quantity}")
                except ApiError as e:
                    print(e.response)
    except Exception as ex:
        print(f"functionError - Erro na atualização dos Blings: {ex}")
    return list_sku


@login_required
def home(request):
    return render(request, 'index.html')


def insert_products(request):
    accounts_blings = AccountBling.objects.all()
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
                            print(f"Conta: {bling.name} | Produto: {sku_codigo} | Estoque: {sku_qtd}")
                    except KeyError:
                        # Father Product
                        logging_future += 1
    except ApiError as e:
        print(e.response)
    return render(request, 'index.html')




