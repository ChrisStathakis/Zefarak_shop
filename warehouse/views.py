from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum

from .models import Store, BillCategory, BillInvoice, Payroll, Invoice
from site_settings.constants import CURRENCY
from .forms import BillInvoiceEditForm, BillInvoiceCreateForm, BillCategoryForm, CreateCopyForm


@method_decorator(staff_member_required, name='dispatch')
class WarehouseDashboard(TemplateView):
    template_name = 'warehouse/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = CURRENCY
        payroll, billing = Payroll.browser.get_queryset().until_today_not_paid(), BillInvoice.broswer.get_queryset().until_today_not_paid()
        billing = billing.aggregate(Sum('final_value'))['final_value__sum'] if billing else 0
        payroll = payroll.aggregate(Sum('final_value'))['final_value__sum'] if payroll else 0
        orders = 30
        general_expenses = 30
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class BillingHomepageView(ListView):
    template_name = 'warehouse/billing/transcation_list_view.html'
    model = BillInvoice

    def get_queryset(self):
        queryset = BillInvoice.broswer.get_queryset().not_paid()
        return queryset[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stores = Store.objects.filter(active=True)
        page_title, list_title, bills = 'Billing Page', 'Billings Per Store', True
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class BillingStoreListView(ListView):
    model = BillInvoice
    template_name = 'warehouse/billing/billing_store_view.html'
    paginate_by = 50

    def get_queryset(self):
        self.instance = get_object_or_404(Store, id=self.kwargs['pk'])
        queryset = BillInvoice.broswer.get_queryset().invoices_per_store(self.instance)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = BillCategory.objects.filter(store=self.instance)
        total_pay = categories.aggregate(Sum('balance'))['balance__sum'] if categories else 0
        total_pay = f'{total_pay} {CURRENCY}'
        instance = self.instance
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class BillInvoiceEditView(UpdateView):
    model = BillInvoice
    form_class = BillInvoiceEditForm
    template_name = 'warehouse/form.html'

    def get_success_url(self):
        my_obj = get_object_or_404(BillInvoice, id=self.kwargs['pk'])
        store = my_obj.category.store
        return reverse('warehouse:billing_store_view', kwargs={'pk': store.id})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The Invoice is Edited Correctly')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object.title}'
        back_url, delete_url = self.get_success_url(), reverse('warehouse:bill_invoice_delete_view', kwargs={'pk': self.object.id})
        create_copy_url = True
        context.update(locals())
        return context


@staff_member_required
def quick_billing_pay(request, pk):
    instance = get_object_or_404(BillInvoice, id=pk)
    instance.is_paid = True
    instance.save()
    messages.success(request, f'The Invoice {instance.title} is paid.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@method_decorator(staff_member_required, name='dispatch')
class CreateBillingInvoiceView(CreateView):
    model = BillInvoice
    template_name = 'warehouse/form.html'
    form_class = BillInvoiceCreateForm

    def get_form(self, *args, **kwargs):
        self.store = get_object_or_404(Store, id=self.kwargs['pk'])
        form = super().get_form(*args, **kwargs)
        form.fields['category'].queryset = BillCategory.objects.filter(store=self.store, active=True)
        return form

    def get_success_url(self):
        self.store = get_object_or_404(Store, id=self.kwargs['pk'])
        return reverse('warehouse:billing_store_view', kwargs={'pk': self.store.id})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The Invoice is Created.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Add new bill to {self.store.title}'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@staff_member_required
def delete_bill_invoice_view(request, pk):
    instance = get_object_or_404(BillInvoice, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:billing_store_view', kwargs={'pk': instance.category.store.id}))


@method_decorator(staff_member_required, name='dispatch')
class CreateBillingCategoryView(CreateView):
    model = BillCategory
    template_name = 'warehouse/form.html'
    form_class = BillCategoryForm

    def get_initial(self):
        self.my_obj = get_object_or_404(Store, id=self.kwargs['pk'])
        initial = super().get_initial()
        initial['store'] = self.my_obj
        return initial

    def get_success_url(self):
        return reverse('warehouse:billing_store_view', kwargs={'pk': self.my_obj.id})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The Bill is created')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create new Bill'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class EditBillingCategoryView(UpdateView):
    model = BillCategory
    template_name = 'warehouse/form.html'
    form_class = BillCategoryForm

    def get_success_url(self):
        self.my_obj = get_object_or_404(BillCategory, id=self.kwargs['pk'])
        return reverse('warehouse:billing_store_view', kwargs={'pk': self.my_obj.store.id})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The Bill is created')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}',
        back_url, delete_url = self.get_success_url(),\
                               reverse('warehouse:bill_category_delete_view',kwargs={'pk': self.kwargs['pk']}
                                                    )

        context.update(locals())
        return context


@staff_member_required
def delete_bill_category_view(request, pk):
    instance = get_object_or_404(BillCategory, id=pk)
    if not instance.bills.exists():
        instance.delete()
    else:
        messages.warning(request, 'You cant delete this.')
    return redirect(reverse('warehouse:billing_store_view', kwargs={'pk': instance.store.id}))


@staff_member_required
def billing_create_copy(request, pk):
    instance = get_object_or_404(BillInvoice, id=pk)
    form_title = 'Create Copy'
    back_url = reverse('warehouse:bill_invoice_edit_view', kwargs={'pk': instance.id})
    form = CreateCopyForm(request.POST or None)
    if form.is_valid():
        days = form.changed_data.get('days', 1)
        months = form.cleaned_data.get('months', None)
        repeat = form.cleaned_data.get('repeat', 1)
        print(days, months, repeat)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = locals()
    return render(request, 'warehouse/form.html')

