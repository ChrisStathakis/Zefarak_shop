from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class HomepageView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('here!')
        return context


class NewProductsView(TemplateView):
    template_name = 'frontend/shop.html'