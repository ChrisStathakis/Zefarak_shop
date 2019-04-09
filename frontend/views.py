from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from site_settings.models import Banner, PaymentMethod, Shipping
from catalogue.models import Product
from .forms import CheckoutForm


class HomepageView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banner = Banner.browser.banner()
        featured_products = Product.my_query.featured_products()
        new_arrivals = Product.my_query.active()[:6]
        context.update(locals())
        return context


class NewProductsView(TemplateView):
    template_name = 'frontend/shop.html'


class ProductView(TemplateView):
    template_name = 'frontend/product-single.html'


class AboutUsView(TemplateView):
    template_name = 'frontend/about.html'


class CartView(TemplateView):
    template_name = 'frontend/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(locals())
        return


class CheckoutView(FormView):
    template_name = 'frontend/checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_methods = PaymentMethod.my_query.active_for_site()
        shipping_methods = Shipping.objects.filter(active=True)

        context.update(locals())
        return context