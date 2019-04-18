from .autocomplete_widgets import VendorAutocomplete, WarehouseCategoryAutocomplete
from django.urls import path

urlpatterns = [
    path('vendors/', VendorAutocomplete.as_view(), name='vendors_auto'),
    path('warehouse/', WarehouseCategoryAutocomplete.as_view(), name='warehouse_category_auto')



]