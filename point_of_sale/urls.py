from django.urls import path
from .views import (DashboardView, OrderListView, CreateOrderView, OrderUpdateView,
                    order_add_product, order_add_product_with_attr, check_product
                    )

app_name = 'point_of_sale'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('order-create/', CreateOrderView.as_view(), name='order_create'),
    path('order-detail/<int:pk>/', OrderUpdateView.as_view(), name='order_detail'),
    path('order/check-add/<int:pk>/<int:dk>/', check_product, name='check_add'),
    path('order/add-product/<int:pk>/<int:dk>/', order_add_product, name='add_product'),
    path('order/add-product-attr/<int:pk>/<int:dk>/', order_add_product_with_attr, name='add_product_attr'),


]