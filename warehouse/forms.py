from django import forms
from datetime import datetime
from .billing import BillInvoice, BillCategory
from .payroll import Employee, Occupation, Payroll
from site_settings.models import Store


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BillInvoiceEditForm(BaseForm, forms.ModelForm):
    date_expired = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    category = forms.ModelChoiceField(required=True, queryset=BillCategory.objects.filter(active=True), widget=forms.HiddenInput())

    class Meta:
        model = BillInvoice
        fields = ['date_expired', 'category', 'title', 'payment_method', 'value', 'is_paid', 'notes']


class BillInvoiceCreateForm(BaseForm, forms.ModelForm):
    date_expired = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = BillInvoice
        fields = ['date_expired', 'category', 'title', 'payment_method', 'value', 'is_paid', 'notes']


class BillCategoryForm(BaseForm, forms.ModelForm):
    store = forms.ModelChoiceField(queryset=Store.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = BillCategory
        fields = ['title', 'store', 'active']


class EmployeeForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['balance', 'date_started', 'vacation_days']


class OccupationForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Occupation
        fields = ['title', 'active', 'store', 'notes']


class PayrollForm(BaseForm, forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), widget=forms.HiddenInput())
    date_expired = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Payroll
        fields = ['date_expired', 'category', 'title', 'payment_method', 'value',
                  'employee', 'is_paid'
                  ]
