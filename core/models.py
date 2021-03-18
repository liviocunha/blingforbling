from django.db import models


class AccountBling(models.Model):
    """
    Accounts of Bling ERP.
    Fields:
        name (str): Name given to Bling Account
        api_key (str): API key provided by Bling
     """
    name = models.CharField(max_length=20)
    api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Persistence of products in the database.
    Fields:
        bling (int): Account linked to the product
        sku (str): Product SKU
        quantity (int): Product stock quantity
        last_update (date): Last stock update
    """
    bling = models.ForeignKey('AccountBling', on_delete=models.CASCADE)
    sku = models.CharField(max_length=30, help_text='Entre com o código SKU do produto.',
                           verbose_name='SKU DO PRODUTO')
    quantity = models.IntegerField(help_text='Entre com a quantidade em estoque.',
                                   verbose_name='ESTOQUE DO PRODUTO')
    last_update = models.DateTimeField(blank=True, help_text='Última atualização de estoque.',
                                       verbose_name='ÚLTIMA ATUALIZAÇÃO')

    def __str__(self):
        return self.sku

    class Meta:
        ordering = ['sku']


class Movement(models.Model):
    """
    Entry and exit movements in product stock.
    Fields:
        quantity (int): Movement quantity
        time (date): Last stock update
        product (int): FK id of product
        after_stock (int): Quantity after movement
        before_stock (int): Quantity before movement
        bling (int): FK id of account Bling
        updated (boolean): It has been updated?
    """
    quantity = models.IntegerField(help_text='Entre com a quantidade da movimentação.',
                                   verbose_name='QUANTIDADE MOVIMENTAÇÃO')
    time = models.DateTimeField(blank=True, help_text='Horário da movimentação.',
                                verbose_name='HORÁRIO DA MOVIMENTAÇÃO')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=False, null=False)
    after_stock = models.IntegerField(help_text='Quantidade do produto depois da movimentação.',
                                      verbose_name='QUANTIDADE DEPOIS')
    before_stock = models.IntegerField(help_text='Quantidade do produto antes da movimentação.',
                                       verbose_name='QUANTIDADE ANTES')
    bling = models.ForeignKey(AccountBling, on_delete=models.CASCADE, blank=False, null=False)
    updated = models.BooleanField(verbose_name='Atualizado nas contas Bling.', default=False)

    class Meta:
        ordering = ['product']
