from django.contrib import admin
from .models import ProductPhotos
from .product_attritubes import (Characteristics, CharacteristicsValue,
                                 ProductCharacteristics,AttributeTitle, Attribute
                                 )


class ProductPhotosInline(admin.TabularInline):
    model = ProductPhotos
    fields = ['image', 'title', 'alt', 'is_primary', 'active']


class ProductCharacteristicsInline(admin.TabularInline):
    model = ProductCharacteristics
    fields = ['title', 'value']


class AttributeInline(admin.TabularInline):
    model = Attribute
    fields = '__all__'
