from django import forms
from catalogue.forms import BaseForm
from catalogue.models import Product


class ProductForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'sku',
                  'brand', 'slug',
                  'price', 'price_discount',
                  'qty', 'qty_measure',
                  'measure_unit',
                  'site_text',
                  'active'
                ]


class ProductNoQty(BaseForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'sku',
                  'brand', 'slug',
                  'price', 'price_discount',
                  'qty_measure', 'measure_unit',
                  'site_text',
                  'active'
                ]
