from django import forms
from site_settings.models import PaymentMethod, Shipping


class CheckoutForm(forms.Form):
    email = forms.EmailField(required=True, label='Email*')
    cellphone = forms.CharField(required=True, label='CellPhone*')
    first_name = forms.CharField(required=True, label='First Name*')
    last_name = forms.CharField(required=True, label='Last Name*')
    address = forms.CharField(required=True, label='Address*')
    city = forms.CharField(required=True, label='City*')
    postcode = forms.CharField(required=True, label='Postcode / ZIP *')
    shipping_method = forms.ModelChoiceField(required=True, queryset=Shipping.objects.filter(active=True))
    payment_method = forms.ModelChoiceField(required=True, queryset=PaymentMethod.my_query.active_for_site())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


