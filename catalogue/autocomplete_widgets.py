from dal import autocomplete
from .product_details import Vendor


class VendorAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Vendor.objects.none()
        qs = Vendor.objects.filter(active=True)
        if self.q:
            qs = qs.filter(title__isstartswith=self.q)
        return qs