from django.urls import path
from .views import DashboardView, OrderListView, CreateOrderView, OrderUpdateView

app_name = 'point_of_sale'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('order-create/', CreateOrderView.as_view(), name='order_create'),
    path('order-detail/<int:pk>/', OrderUpdateView.as_view(), name='order_detail'),

]