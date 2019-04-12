from django.shortcuts import reverse, redirect, render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from .models import Invoice
from catalogue.product_details import Vendor
from .forms import CreateInvoiceForm


@method_decorator(staff_member_required, name='dispatch')
class WarehouseOrderList(ListView):
    model = Invoice
    template_name = 'warehouse/invoices/list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = Invoice.objects.all()
        queryset = Invoice.filter_data(self.request, queryset)
        return queryset


@staff_member_required
def create_warehouse_order_view(request):
    form = CreateInvoiceForm(request.POST or None)
    form_title = 'Create New Invoice'
    back_url = reverse('warehouse:invoices')

    return render(request, 'warehouse/form.html', locals())


@method_decorator(staff_member_required, name='dispatch')
class UpdateWarehouseOrderView(UpdateView):
    pass


@staff_member_required
def delete_warehouse_order_view(request, pk):
    pass


@method_decorator(staff_member_required, name='dispatch')
class VendorListView(ListView):
    model = Vendor
    template_name = ''
    paginate_by = 50


@method_decorator(staff_member_required, name='dispatch')
class VendorCreateView(CreateView):
    model = Vendor
    form_class = ''
    template_name = 'warehouse/form.html'


@method_decorator(staff_member_required, name='dispatch')
class VendorUpdateView(UpdateView):
    model = Vendor
    form_class = ''
    template_name = 'warehouse/form.html'


@staff_member_required
def delete_vendor(request, pk):
    instance = get_object_or_404(Vendor, id=pk)
    instance.delete()
    return redirect('')