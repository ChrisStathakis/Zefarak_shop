from django import forms
from .models import Order

class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class OrderCreateForm(BaseForm, forms.ModelForm):
    date_expired = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ['date_expired', 'order_type', 'user', 'payment_method']

