from django import forms

from .models import User, Profile


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(BaseForm):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProfileForm(BaseForm, forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'user',
                  'shipping_address', 'shipping_city', 'shipping_zip_code',
                  'billing_address', 'billing_city', 'billing_zip_code',
                  'cellphone', 'phone', 'value'
                  ]
