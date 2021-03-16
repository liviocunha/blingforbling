from django.urls import path
from .views import HookInventoryChangeView

urlpatterns = [
    path('hookinventory/', HookInventoryChangeView.as_view(), name='Hook Inventory Change')
]

