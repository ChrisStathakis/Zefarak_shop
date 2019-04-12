from django import forms
from django.forms import formset_factory
from .models import Attribute


class CartAttributeForm(forms.Form):
    attributes = forms.ModelChoiceField(queryset=Attribute.objects.all())


CartAttributeFormset = formset_factory(CartAttributeForm, extra=2)
