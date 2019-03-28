from django.urls import path
from .views import HomepageView, NewProductsView

urlpatterns = [
   path('', HomepageView.as_view(), name='homepage'),
   path('new-products/', NewProductsView.as_view(), name='new_products')

]

