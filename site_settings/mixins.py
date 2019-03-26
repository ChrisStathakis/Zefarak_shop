from django.views.generic import FormView
from django.shortcuts import reverse
from django.contrib import messages


class StoreBaseMixin(FormView):

    def get_success_url(self):
        return reverse('site_settings:stores')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The item have been manipulated.')
        return super().form_valid(form)


class PaymentBaseMixin(FormView):

    def get_success_url(self):
        return reverse('site_settings:payment_methods')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The item have been manipulated.')
        return super().form_valid(form)


class ShippingBaseMixin(FormView):

    def get_success_url(self):
        return reverse('site_settings:shipping')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The item have been manipulated.')
        return super().form_valid(form)
