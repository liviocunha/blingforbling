from django.contrib import admin
from core.models import Bling, Product, Movement


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'bling', 'quantity', 'last_update')
    search_fields = ('bling__name', 'sku')


class MovementAdmin(admin.ModelAdmin):
    list_display = ('time', 'quantity', 'bling', 'product', 'after_stock', 'before_stock', 'updated')
    search_fields = ('product__sku', 'bling__name', 'update')


class BlingAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key')
    search_fields = ('name', )


admin.site.register(Product, ProductAdmin)
admin.site.register(Movement, MovementAdmin)
admin.site.register(Bling, BlingAdmin)
