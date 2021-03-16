import json
from django.http import HttpResponse
from django.views.generic import View

from braces.views import CsrfExemptMixin


class HookInventoryChangeView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        sku = data['retorno']['estoques'][0]['estoque']['codigo']
        estoque_atual = data['retorno']['estoques'][0]['estoque']['estoqueAtual']
        print(f"Produto: {sku} | Estoque Atual: {estoque_atual}")

        return HttpResponse('\n OK! Status Code 200 \n')
