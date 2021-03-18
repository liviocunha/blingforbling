from django.urls import path, include
from .views import HookInventoryChangeView1, HookInventoryChangeView2, home, insert_products

urlpatterns = [
    path('', home),
    path('hookinventory/1/', HookInventoryChangeView1.as_view(), name='Hook Inventory Change Bling 1'),
    path('hookinventory/2/', HookInventoryChangeView2.as_view(), name='Hook Inventory Change Bling 2'),
    path('insertProducts/', insert_products),
    path('accounts/', include('django.contrib.auth.urls'))
]
