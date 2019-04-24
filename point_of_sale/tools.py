from django import forms
from catalogue.product_attritubes import Attribute


def generate_or_remove_queryset(form, title_list, queryset):
    fields_added = []
    for title in title_list:
        items = queryset.filter(class_related__title__icontains=title)
        if items.exists():
            print(title)
            form.fields[title].queryset = items.first().my_attributes.all()
            fields_added.append(title)
        else:
            form.fields[title] = forms.ModelChoiceField(queryset=Attribute.objects.all(), widget=forms.HiddenInput(), required=False)
    return fields_added