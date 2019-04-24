from django import forms
from django.conf import settings
from catalogue.forms import BaseForm
from catalogue.models import Product

from dal import autocomplete

WAREHOUSE_ORDERS_TRANSCATIONS = settings.WAREHOUSE_ORDERS_TRANSCATIONS
RETAIL_TRANSCATIONS = settings.RETAIL_TRANSCATIONS


class ProductForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['active', 'featured_product',
                 'title', 'sku',
                  'vendor', 'order_code',
                  'price_buy', 'order_discount',
                  'brand', 'category',
                  'price', 'price_discount',
                  'qty_measure',
                  'measure_unit',
                  'site_text', 'slug'

                  ]
        widgets = {
            'vendor': autocomplete.ModelSelect2(url='vendors_auto', attrs={'class': 'form-control'}),
            'category': autocomplete.ModelSelect2(url='warehouse_category_auto',
                                                  attrs={'class': 'form-control', 'data-html': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not WAREHOUSE_ORDERS_TRANSCATIONS and RETAIL_TRANSCATIONS:
            self.fields['qty_add'] = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
        if WAREHOUSE_ORDERS_TRANSCATIONS and not RETAIL_TRANSCATIONS and not self.instance.product_class.is_service:
            self.fields['qty_remove'] = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

'''
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

'''

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
