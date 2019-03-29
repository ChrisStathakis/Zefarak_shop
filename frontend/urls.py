from django.urls import path
from .views import HomepageView, NewProductsView, ProductView, AboutUsView, CartView, CheckoutView

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('new-products/', NewProductsView.as_view(), name='new_products'),
    path('product/', ProductView.as_view(), name='product_view'),
    path('cart/', CartView.as_view(), name='cart_page'),
    path('about/', AboutUsView.as_view(), name='about_page'),
    path('checkout/', CheckoutView.as_view(), name='checkout_page'),

]

