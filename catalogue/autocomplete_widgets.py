from dal import autocomplete
from .product_details import Vendor
from .models import WarehouseCategory
from django.utils.html import format_html


class VendorAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Vendor.objects.none()
        qs = Vendor.objects.all()
        if self.q:
            qs = qs.filter(title__isstartswith=self.q)
        return qs


class WarehouseCategoryAutocomplete(autocomplete.Select2QuerySetView):

    def get_result_label(self, item):
        return format_html(f'<span class="form-control" id="select2-id_vendor-container" title={item.title}><span class="select2-selection__clear">×</span>{item.title}</span>')

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return WarehouseCategory.objects.none()
        qs = WarehouseCategory.objects.all()
        if self.q:
            qs = qs.filter(title__startswith=self.q)
        return qs
