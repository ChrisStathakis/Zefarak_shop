from django import forms
from .models import *
from .product_attritubes import CharacteristicsValue, Characteristics, AttributeClass, AttributeTitle, ProductCharacteristics, Attribute
from .models import Product, ProductPhotos
from .product_details import Vendor, VendorPaycheck

from dal import autocomplete


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'product_class']

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CreateProductClassForm(forms.ModelForm):

    class Meta:
        model = ProductClass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CreateProductClassForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CategorySiteForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CharacteristicsValueForm(BaseForm, forms.ModelForm):
    char_related = forms.ModelChoiceField(queryset=Characteristics.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = CharacteristicsValue
        fields = ['title', 'char_related', 'custom_ordering']


class CharacteristicsForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Characteristics
        fields = ['active', 'title', 'custom_ordering']


class AttributeClassForm(BaseForm, forms.ModelForm):

    class Meta:
        model = AttributeClass
        fields = '__all__'


class AttributeTitleForm(BaseForm, forms.ModelForm):
    attri_by = forms.ModelChoiceField(queryset=AttributeClass.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = AttributeTitle
        fields = '__all__'


class ProductForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'sku',
                  'vendor', 'order_code',
                  'brand', 'slug',
                  'price', 'price_discount',
                  'qty', 'qty_measure',
                  'site_text',
                  'active', 'featured_product'
                   ]


class ProductPhotoUploadForm(forms.Form):
    image = forms.ImageField()


class ProductCharacteristicForm(BaseForm, forms.ModelForm):
    product_related = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())
    title = forms.ModelChoiceField(queryset=Characteristics.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = ProductCharacteristics
        fields = '__all__'


class AttributeForm(forms.ModelForm):

    class Meta:
        model = Attribute
        fields = '__all__'


class VendorForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Vendor
        fields = '__all__'
        exclude = ['balance', 'remaining_deposit']


class PaycheckVendorForm(BaseForm, forms.ModelForm):
    date_expired = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = VendorPaycheck
        fields = ['date_expired', 'vendor', 'payment_method', 'title', 'is_paid', 'value']
        widgets = {
            'vendor': autocomplete.ModelSelect2(url='vendors_auto', attrs={'class': 'form-control'})
        }
