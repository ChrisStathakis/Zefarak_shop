from django.urls import path
from .views import (DashboardView, OrderListView, EshopListView, CreateOrderView, OrderUpdateView, delete_order,
                    order_add_product, order_add_product_with_attr, check_product, add_to_order_with_attr,
                    order_item_edit_with_attr
                    )
from .ajax_views import ajax_order_item, ajax_search_products, ajax_add_product
from .views_actions import create_retail_order_view
app_name = 'point_of_sale'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('eshop-orders/', EshopListView.as_view(), name='eshop_list'),
    path('order-create/', CreateOrderView.as_view(), name='order_create'),
    path('order-detail/<int:pk>/', OrderUpdateView.as_view(), name='order_detail'),
    path('order-detail/<int:pk>/delete/', delete_order, name='delete_order'),
    path('order/check-add/<int:pk>/<int:dk>/', check_product, name='check_add'),
    path('order/add-product/<int:pk>/<int:dk>/', order_add_product, name='add_product'),
    path('order/add-product-attr/<int:pk>/<int:dk>/', order_add_product_with_attr, name='add_product_attr'),
    path('order/add-product-attr/<int:pk>/<int:dk>/<int:lk>/', add_to_order_with_attr, name='add_to_order_attr'),
    path('order/edit-order-item-with-att/<int:pk>/', order_item_edit_with_attr, name='edit_order_item_attr'),

    #  ajax calls
    path('order/ajax/edit-order-item/<slug:action>/<int:pk>/', ajax_order_item, name='ajax_order_item_edit'),
    path('ajax/search-items/<int:pk>/', ajax_search_products, name='ajax_search'),
    path('ajax/search-items/<int:pk>/<int:dk>/', ajax_add_product, name='ajax_add_product'),

    #  actions
    path('action/create-order/', create_retail_order_view, name='action_create_order')

]