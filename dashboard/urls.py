from django.contrib import admin
from django.urls import path, include, re_path

from .views import (DashBoard, ProductsListView, ProductCreateView,
                    product_detail, CategorySiteManagerView, ProductMultipleImagesView, CharacteristicsManagerView,
                    ProductCharacteristicCreateView, ProductAttributeManagerView, create_attr_product_class,
                    ProductAttriClassManagerView, RelatedProductsView, product_characteristic_delete_view
                    )

from .settings_view import (ProductClassView, ProductClassCreateView,
                            CategorySiteListView, CategorySiteEditView, CategorySiteCreateView, delete_category_site,
                            BrandListView, BrandEditView, BrandCreateView, delete_brand,
                            CharacteristicsListView, characteristics_detail_view, CharacterCreateView,
                            characteristic_delete_view, CharValueEditView, delete_char_value_view,
                            AttributeClassListView, attribute_class_edit_view, attribute_class_delete_view,
                            AttributeClassCreateView, attribute_title_delete_view, AttributeTitleEditView,
                            )
from .dashboard_actions import copy_product_view
from .ajax_views import (ajax_category_site, ajax_product_images, ajax_add_or_delete_attribute,
                         ajax_change_qty_on_attribute,
                         popup_category, popup_brand
                         )
app_name = 'dashboard'


urlpatterns = [
    path('', DashBoard.as_view(), name='home'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/detail/<int:pk>/', product_detail, name='product_detail'),
    path('product/category-site-manager/<int:pk>/', CategorySiteManagerView.as_view(), name='category_manager_view'),
    path('add-multiply-images/<int:pk>/', ProductMultipleImagesView.as_view(), name='image_manager_view'),

    #popups
    path('product/popups/create-category/', popup_category, name='popup_category'),
    path('product/popups/create-brand/', popup_brand, name='popup_brand'),

    # actions
    path('products/copy/<int:pk>/',copy_product_view, name='copy_product'),

    path('product/characteristic-manager/<int:pk>/', CharacteristicsManagerView.as_view(), name='char_manager_view'),
    path('product/chara-create/<int:pk>/<int:dk>/', ProductCharacteristicCreateView.as_view(), name='product_char_create_view'),

    path('product/attribute-manager/<int:pk>/', ProductAttributeManagerView.as_view(), name='attribute_manager_view'),
    path('product/attribute-create/<int:pk>/<int:dk>/', create_attr_product_class, name='product_create_attr_view'),
    path('product/attribute-detail/<int:pk>/', ProductAttriClassManagerView.as_view(), name='product_attr_detail_view'),

    path('product/related/<int:pk>/', RelatedProductsView.as_view(), name='related_products_manager_view'),


    path('ajax/category-site-manager/<slug:slug>/<int:pk>/<int:dk>/', ajax_category_site, name='ajax_category_site'),
    path('ajax/image-manager/<slug:slug>/<int:pk>/<int:dk>/', ajax_product_images, name='ajax_image'),
    path('ajax/add-or-delete-attr/<slug:slug>/<int:pk>/<int:dk>/', ajax_add_or_delete_attribute, name='ajax_manage_attribute'),
    path('ajax/add-qty/<int:pk>/', ajax_change_qty_on_attribute, name='ajax_manage_qty_attribute'),


    path('product/characteristic-manager/<int:pk>/', CharacteristicsManagerView.as_view(), name='char_manager_view'),
    path('product/delete/<int:pk>/', product_characteristic_delete_view, name='product_char_delete_view'),

    path('product-class-list/', ProductClassView.as_view(), name='product_class_view'),
    path('products-class-create/', ProductClassCreateView.as_view(), name='product_class_create_view'),

    path('category-list/', CategorySiteListView.as_view(), name='category_list'),
    path('category-edit/<int:pk>/', CategorySiteEditView.as_view(), name='category_edit_view'),
    path('category-create/', CategorySiteCreateView.as_view(), name='category_create_view'),
    path('category-delete/<int:pk>/', delete_category_site, name='delete_category_site'),

    path('brand-list/', BrandListView.as_view(), name='brand_list_view'),
    path('brand-edit/<int:pk>/', BrandEditView.as_view(), name='brand_edit_view'),
    path('brand-create/', BrandCreateView.as_view(), name='brand_create_view'),
    path('brand-delete/<int:pk>/', delete_brand, name='delete_brand'),

    path('characteristics/', CharacteristicsListView.as_view(), name='characteristics_list_view'),
    path('characteristics/detail/<int:pk>/', characteristics_detail_view, name='char_edit_view'),
    path('characteristics/create/', CharacterCreateView.as_view(), name='char_create_view'),
    path('characteristics/delete/<int:pk>/', characteristic_delete_view, name='char_delete_view'),
    path('characteristics/value/edit/<int:pk>/', CharValueEditView.as_view(), name='char_value_edit_view'),
    path('characteristics/value/delete/<int:pk>/', delete_char_value_view, name='char_value_delete_view'),

    path('atributes-class/list/', AttributeClassListView.as_view(), name='attribute_class_list_view'),
    path('atributes-class/create/', AttributeClassCreateView.as_view(), name='attribute_class_create_view'),
    path('atributes-class/delete//<int:pk>/', attribute_class_delete_view, name='attribute_class_delete_view'),
    path('atributes-class/edit/<int:pk>/', attribute_class_edit_view, name='attribute_class_edit_view'),

    path('atributes-title/edit/<int:pk>/', AttributeTitleEditView.as_view(), name='attribute_title_edit_view'),
    path('atributes-title/delete/<int:pk>/', attribute_title_delete_view, name='attribute_title_delete_view'),




    ]
