from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from .models import Invoice, InvoiceOrderItem
from catalogue.models import Product
from catalogue.product_details import Vendor
from catalogue.forms import VendorForm
from .forms import CreateInvoiceForm, UpdateInvoiceForm, CreateOrderItemForm


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
    if form.is_valid():
        instance = form.save()
        return redirect(instance.get_edit_url())

    return render(request, 'warehouse/form.html', locals())


@method_decorator(staff_member_required, name='dispatch')
class UpdateWarehouseOrderView(UpdateView):
    model = Invoice
    template_name = 'warehouse/invoices/order_detail.html'
    form_class = UpdateInvoiceForm
    success_url = reverse_lazy('warehouse:invoices')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.my_query.active().filter(vendor=self.object.vendor)
        instance = self.object
        context.update(locals())
        return context


@staff_member_required
def create_or_add_order_item(request, pk, dk):
    instance = get_object_or_404(Invoice, id=pk)
    product = get_object_or_404(Product, id=dk)
    order_item = InvoiceOrderItem.objects.filter(order=instance, product=product)
    if not order_item.exists():
        return 'fave attr' if product.have_attr else redirect(reverse('warehouse:create-order-item', kwargs={'pk': pk,
                                                                                                             'dk': dk})
                                                              )
    return 'fave attr' if product.have_attr else redirect(reverse('warehouse:create-order-item'))


@method_decorator(staff_member_required, name='dispatch')
class CreateOrderItem(CreateView):
    model = InvoiceOrderItem
    form_class = CreateOrderItemForm
    template_name = 'warehouse/form.html'

    def get_success_url(self):
        return reverse('warehouse:update_order', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        self.instance = get_object_or_404(Invoice, id=self.kwargs['pk'])
        self.product = get_object_or_404(Product, id=self.kwargs['dk'])
        initial = super().get_initial()
        initial['order'] = self.instance
        initial['product'] = self.product
        initial['sku'] = self.product.order_code
        initial['value'] = self.product.price_buy
        initial['discount_value'] = self.product.order_discount
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Add {self.product} to {self.instance}'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class UpdateInvoiceOrderItem(UpdateView):
    model = InvoiceOrderItem
    form_class = CreateOrderItemForm
    template_name = 'warehouse/form.html'

    def get_success_url(self):
        return reverse('warehouse:update_order', kwargs={'pk': self.object.order.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = self.get_success_url(), reverse('warehouse:order-item-delete', kwargs={'pk': self.object.id})
        context.update(locals())
        return  context


@staff_member_required
def delete_warehouse_order_item_view(request, pk):
    instance = get_object_or_404(InvoiceOrderItem, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:update_order', kwargs={'pk': instance.order.id}))

@staff_member_required
def delete_warehouse_order_view(request, pk):
    instance = get_object_or_404(InvoiceOrderItem, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:update_order', kwargs={'pk': instance.order.id}))


@method_decorator(staff_member_required, name='dispatch')
class VendorListView(ListView):
    model = Vendor
    template_name = 'warehouse/invoices/vendor_list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = Vendor.objects.all()
        queryset = Vendor.filter_data(self.request, queryset)
        return queryset


@method_decorator(staff_member_required, name='dispatch')
class VendorCreateView(CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:vendors')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        back_url, delete_url = self.success_url, None
        form_title = 'Create new Vendor'
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class VendorUpdateView(UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:vendors')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        back_url, delete_url = reverse('warehouse:vendors'), reverse('warehouse:vendor_delete', kwargs={'pk': self.kwargs['pk']})
        form_title = f'Edit {self.object}'
        context.update(locals())
        return context


@staff_member_required
def delete_vendor(request, pk):
    instance = get_object_or_404(Vendor, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:vendors'))