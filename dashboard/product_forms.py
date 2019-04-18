from django import forms
from catalogue.forms import BaseForm
from catalogue.models import Product

from dal import autocomplete


class ProductForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'sku',
                  'vendor', 'order_code',
                  'price_buy', 'order_discount',
                  'brand', 'category',
                  'price', 'price_discount',
                  'qty', 'qty_measure',
                  'measure_unit',
                  'site_text', 'slug',
                  'active', 'featured_product'
                ]
        widgets = {
            'vendor': autocomplete.ModelSelect2(url='vendors_auto', attrs={'class': 'form-control'}),
            'category': autocomplete.ModelSelect2(url='warehouse_category_auto', attrs={'class': 'form-control', 'data-html': True}),
        }


class ProductNoQty(BaseForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'sku',
                  'vendor', 'order_code',
                  'price_buy', 'order_discount',
                  'brand', 'category',
                  'price', 'price_discount',
                  'qty_measure', 'measure_unit',
                  'site_text', 'slug',
                  'active', 'featured_product'
                ]
        widgets = {
            'vendor': autocomplete.ModelSelect2(url='vendors_auto', attrs={'class': 'form-control'}),
            'category': autocomplete.ModelSelect2(url='warehouse_category_auto', attrs={'class': 'form-control'}),
        }
