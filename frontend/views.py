from django.shortcuts import render
from django.views.generic import TemplateView

from site_settings.models import Banner
from catalogue.models import Product


class HomepageView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banner = Banner.browser.banner()
        featured_products = Product.my_query.featured_products()
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


class CheckoutView(TemplateView):
    template_name = 'frontend/checkout.html'