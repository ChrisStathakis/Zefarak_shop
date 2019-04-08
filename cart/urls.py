from django.urls import path
from .views import CartListView, CartDetailView, check_cart_movement

app_name = 'cart'

urlpatterns = [
    #  dashboard urls
    path('', CartListView.as_view(), name='cart_list'),
    path('detail/<int:pk>/', CartDetailView.as_view(), name='cart_detail'),

    path('check/<int:pk>/<slug:action>/', check_cart_movement, name='check'),
    ]