from django import forms
from catalogue.forms import BaseForm
from catalogue.models import Product


class ProductForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'sku',
                  'vendor', 'order_code',
                  'brand', 'slug',
                  'price', 'price_discount',
                  'qty', 'qty_measure',
                  'measure_unit',
                  'site_text',
                  'active', 'featured_product'
                ]


class ProductNoQty(BaseForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'sku',
                  'vendor', 'order_code',
                  'brand', 'slug',
                  'price', 'price_discount',
                  'qty_measure', 'measure_unit',
                  'site_text',
                  'active', 'featured_product'
                ]
