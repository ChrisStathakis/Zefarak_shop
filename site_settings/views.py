from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from .mixins import StoreBaseMixin, PaymentBaseMixin, ShippingBaseMixin
from .models import Store, PaymentMethod, Shipping
from .forms import StoreForm, PaymentMethodForm, ShippingForm


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'site_settings/dashboard.html'


@method_decorator(staff_member_required, name='dispatch')
class StoreListView(ListView):
    template_name = 'site_settings/list_view.html'
    model = Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = 'Store'
        create_url = reverse('site_settings:store_create')
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class StoreCreateView(StoreBaseMixin, CreateView):
    model = Store
    template_name = 'site_settings/form.html'
    form_class = StoreForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create Store'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class StoreEditView(StoreBaseMixin, UpdateView):
    model = Store
    template_name = 'site_settings/form.html'
    form_class = StoreForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodListView(ListView):
    model = PaymentMethod
    template_name = 'site_settings/list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = 'Payment Method'
        create_url = reverse('site_settings:payment_create')
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodCreateView(PaymentBaseMixin, CreateView):
    model = PaymentMethod
    template_name = 'site_settings/form.html'
    form_class = PaymentMethodForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create Payment'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodUpdateView(UpdateView):
    model = PaymentMethod
    template_name = 'site_settings/form.html'
    form_class = PaymentMethodForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class ShippingListView(ListView):
    model = Shipping
    template_name = 'site_settings/list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = 'Shipping'
        create_url = reverse('site_settings:shipping_create')
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class ShippingCreateView(ShippingBaseMixin, CreateView):
    model = Shipping
    template_name = 'site_settings/form.html'
    form_class = ShippingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create New Shipping'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class ShippingEditView(ShippingBaseMixin, UpdateView):
    model = Shipping
    template_name = 'site_settings/form.html'
    form_class = ShippingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context
