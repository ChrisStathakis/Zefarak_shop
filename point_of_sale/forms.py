from django import forms
from .models import Order, OrderItem, OrderItemAttribute
from catalogue.models import Product
from catalogue.product_attritubes import Attribute
from dal import autocomplete


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderCreateForm(BaseForm, forms.ModelForm):
    date_expired = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ['date_expired', 'status', 'payment_method', 'shipping']


class OrderUpdateForm(BaseForm, forms.ModelForm):
    date_expired = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ['is_paid', 'discount', 'date_expired', 'title', 'payment_method', 'status', 'profile']
        widgets = {
            'profile': autocomplete.ModelSelect2(url='point_of_sale:autocomplete_profile', attrs={'class': 'form-control', })
        }


class OrderItemCreateForm(BaseForm, forms.ModelForm):
    title = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
    order = forms.ModelChoiceField(queryset=Order.objects.all(), widget=forms.HiddenInput())
    attribute = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = OrderItem
        fields = ['title', 'order', 'qty', 'attribute']


class OrderItemAttrForm(BaseForm, forms.ModelForm):

    class Meta:
        model = OrderItemAttribute
        fields = '__all__'


class OrderChangeTitle(BaseForm, forms.ModelForm):

    class Meta:
        model = Order
        fields = ['title', ]


class OrderItemCoffeeForm(BaseForm, forms.Form):
    sugar = forms.ModelChoiceField(queryset=Attribute.objects.all())
    sugar_lvl = forms.ModelChoiceField(queryset=Attribute.objects.all())
    milk = forms.ModelChoiceField(queryset=Attribute.objects.all())
    ingredient = forms.ModelChoiceField(queryset=Attribute.objects.all())
    qty = forms.IntegerField()
