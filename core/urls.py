from django.urls import path, include
from .views import HookInventoryChangeView, home, insert_products

urlpatterns = [
    path('', home),
    path('hookinventory/', HookInventoryChangeView.as_view(), name='Hook Inventory Change'),
    path('insertProducts/', insert_products),
    path('accounts/', include('django.contrib.auth.urls'))
]
