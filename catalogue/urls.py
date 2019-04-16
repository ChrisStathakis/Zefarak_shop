from .autocomplete_widgets import VendorAutocomplete
from django.urls import path

urlpatterns = [
    path('vendors/', VendorAutocomplete.as_view(), name='vendors_auto'),



]