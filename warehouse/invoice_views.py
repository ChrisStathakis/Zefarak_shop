from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, F
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Invoice, InvoiceOrderItem, InvoiceImage
from catalogue.models import Product
from catalogue.product_details import Vendor, VendorPaycheck
from catalogue.forms import VendorForm, PaycheckVendorForm
from site_settings.constants import CURRENCY
from .forms import CreateInvoiceForm, UpdateInvoiceForm, CreateOrderItemForm, InvoiceImageForm
from .tables import InvoiceImageTable, PaycheckTable

from django_tables2 import RequestConfig


@method_decorator(staff_member_required, name='dispatch')
class WarehouseOrderList(ListView):
    model = Invoice
    template_name = 'warehouse/invoices/list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = Invoice.objects.all()
        queryset = Invoice.filter_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendors = Vendor.objects.filter(active=True)
        context.update(locals())
        return context


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
        images = InvoiceImage.objects.filter(order_related=self.object)
        images_table = InvoiceImageTable(images)
        RequestConfig(self.request).configure(images_table)
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
        return context


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


@method_decorator(staff_member_required, name='dispatch')
class PayCheckListView(ListView):
    model = VendorPaycheck
    template_name = 'warehouse/invoices/paycheck_list.html'
    paginate_by = 50

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        vendors = Vendor.objects.filter(active=True)
        payment_checks = PaycheckTable(self.object_list)
        RequestConfig(self.request).configure(payment_checks)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaycheckDetailView(UpdateView):
    model = VendorPaycheck
    form_class = PaycheckVendorForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:paychecks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = self.success_url, self.object.get_delete_url
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaycheckCreateView(CreateView):
    model = VendorPaycheck
    form_class = PaycheckVendorForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:paychecks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create New Payment'
        back_url, delete_url = self.success_url, None
        context.update(locals())
        return context


@staff_member_required
def delete_paycheck(request, pk):
    pass


@method_decorator(staff_member_required, name='dispatch')
class CreateInvoiceImageView(CreateView):
    model = InvoiceImage
    form_class = InvoiceImageForm
    template_name = 'warehouse/form.html'

    def get_success_url(self):
        return reverse('warehouse:update_order', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        initial = super().get_initial()
        order = get_object_or_404(Invoice, id=self.kwargs['pk'])
        initial['order_related'] = order
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create new Image'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class UpdateInvoiceImageView(UpdateView):
    model = InvoiceImage
    form_class = InvoiceImageForm
    template_name = 'warehouse/form.html'

    def get_success_url(self):
        return reverse('warehouse:update_order', kwargs={'pk': self.object.order_related.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = self.get_success_url(), reverse('warehouse:delete-order-image', kwargs={'pk': self.object.id})
        context.update(locals())
        return context


@staff_member_required
def delete_invoice_image_view(request, pk):
    instance = get_object_or_404(InvoiceImage, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:update_order', kwargs={'pk': instance.order_related.id}))


@staff_member_required
def ajax_calculate_value(request, question):
    page_title, my_data = '', []
    queryset = Invoice.objects.all()
    queryset = Invoice.filter_data(request, queryset)
    data = dict()
    if question == 'value':
        page_title = 'Analysis Value'
        total_value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset.exists() else 0
        paid_value = queryset.aggregate(Sum('paid_value'))['paid_value__sum'] if queryset.exists() else 0
        paid_value = total_value- paid_value
        paid_value = f'{paid_value} {CURRENCY}'
        total_value = f'{total_value} {CURRENCY}'
        my_data = [('Total Value', total_value), ('You own', paid_value)]
    if question == 'vendors':
        my_data = queryset.values_list('vendor__title').annotate(remaning=Sum(F('final_value')-F('paid_value')),
                                                                 total=Sum('final_value')).order_by('total')
        print(my_data)
        page_title = 'Vendor analysis'
    data['result'] = render_to_string(request=request,
                                      template_name='warehouse/ajax/invoice_results.html',
                                      context={'page_title': page_title,
                                               'my_data': my_data,
                                               'question': question
                                               }
                                      )
    return JsonResponse(data)
