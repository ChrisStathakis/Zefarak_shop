from django.urls import path
from .views import HomepageView, NewProductsView, product_view, AboutUsView, CartView, CheckoutView, order_detail

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('new-products/', NewProductsView.as_view(), name='new_products'),
    path('product/<slug:slug>/', product_view, name='product_view'),
    path('cart/', CartView.as_view(), name='cart_page'),
    path('about/', AboutUsView.as_view(), name='about_page'),
    path('checkout/', CheckoutView.as_view(), name='checkout_page'),
    path('order-detail/<int:pk>/', order_detail, name='order_detail')

]

