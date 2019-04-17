from django.contrib import admin
from django.conf import settings
from .models import ProductClass, Product, ProductPhotos
from .product_details import Vendor, Brand
from .categories import Category, WarehouseCategory
from .product_attritubes import (Characteristics, CharacteristicsValue,
                                 ProductCharacteristics, AttributeTitle, Attribute,
                                 AttributeClass, AttributeProductClass
                                 )
from .product_details import VendorPaycheck
from .inlines import ProductCharacteristicsInline, ProductPhotosInline

from mptt.admin import DraggableMPTTAdmin


WAREHOUSE_ORDERS_TRANSCATIONS = settings.WAREHOUSE_ORDERS_TRANSCATIONS


@admin.register(VendorPaycheck)
class VendorPaycheckAdmin(admin.ModelAdmin):
    pass

@admin.register(Characteristics)
class CharacteristicsAdmin(admin.ModelAdmin):
    pass


@admin.register(CharacteristicsValue)
class CharacteristicsValueAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCharacteristics)
class ProductCharacteristicsAdmin(admin.ModelAdmin):
    pass


@admin.register(AttributeClass)
class AttributeClassAdmin(admin.ModelAdmin):
    pass


@admin.register(AttributeTitle)
class AttributeTitlesAdmin(admin.ModelAdmin):
    pass


@admin.register(AttributeProductClass)
class AttributeTitlesAdmin(admin.ModelAdmin):
    pass


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['have_attribute', 'have_transcations', 'is_service']
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields = ['have_attribute', 'have_transcations', 'is_service']
        return readonly_fields


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'active', ]
    search_fields = ['name', ]
    list_filter = ['active']
    list_display_links = ['indented_title', ]
    list_per_page = 30
    readonly_fields = ['parent', ]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['title', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_class', 'tag_final_price', 'qty', 'active']
    list_filter = ['active', 'is_offer', 'category']
    filter_horizontal = ['related_products', 'category_site', ]
    list_select_related = ['category', 'brand']
    readonly_fields = ['tag_final_price', 'is_offer']
    autocomplete_fields = ['brand', ]
    save_as = True
    list_per_page = 50
    search_fields = ['title']
    inlines = [ProductPhotosInline, ProductCharacteristicsInline]
    fieldsets = (
        ('Αποθήκη', {
            'fields': (('active', 'product_class', 'is_offer'),
                       ('title', 'brand', 'sku'),
                       'category_site',
                       ('price', 'price_discount', 'tag_final_price'),
                       ('qty', 'qty_kilo', 'measure_unit'),
                       )
        }),

        ('Site', {
            'fields': (
                ('slug', 'site_text'),
                ('related_products',)
            )
        }),

    )

    def get_readonly_fields(self, request, obj=None):
        read_only = self.readonly_fields
        if obj:
            read_only.append('product_class')
        if WAREHOUSE_ORDERS_TRANSCATIONS:
            read_only.append('vendor')
        return read_only

    def save_model(self, request, obj, form, change):
        if '_saveasnew' in request.POST:
            obj.slug = None
            return super(ProductAdmin, self).save_model(request, obj, form, change)
        return super(ProductAdmin, self).save_model(request, obj, form, change)


@admin.register(ProductPhotos)
class ProductPhotosAdmin(admin.ModelAdmin):
    list_display = ['tag_image_tiny', 'title', 'is_primary', 'active']
    readonly_fields = ['tag_image_tiny', 'tag_image']
    list_filter = ['is_primary', 'active']
    search_fields = ['product__title']
    list_per_page = 50
    autocomplete_fields = ['product']
    fields = ['is_primary', 'active', 'tag_image', 'image', 'product', 'title', 'alt']


#  warehouse admin

@admin.register(WarehouseCategory)
class WarehouseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ['active', ]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vat', 'phone', 'tag_balance', 'active']
    list_filter = ['active', ]
    search_fields = ['title', 'email', 'phone', 'cellphone']
    list_per_page = 30


if not WAREHOUSE_ORDERS_TRANSCATIONS:
    admin.site.unregister(WarehouseCategory)
    admin.site.unregister(Vendor)

