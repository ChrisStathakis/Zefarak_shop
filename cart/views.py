from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DetailView

from django.contrib import messages
from .tools import check_or_create_cart
# Create your views here.
from catalogue.models import Product
from .models import CartItem, Cart


class CartListView(ListView):
    model = Cart
    template_name = 'cart/listview.html'

    def get_queryset(self):
        queryset = Cart.objects.all()

        return queryset


class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart/listview.html'


def add_to_cart_with_attr():
    print('here')


def add_to_cart(request, product):
    cart = check_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if created:
        cart_item.qty = 1
        cart_item.value = product.price
        cart_item.price_discount = product.price_discount
    else:
        cart_item.qty += 1
    cart_item.save()


def remove_from_cart_with_attr():
    print('delete')


def check_cart_movement(request, pk, action):
    if action is 'add':
        product = get_object_or_404(Product, id=pk)
        add_to_cart_with_attr() if product.have_attr else add_to_cart(request, product)
        messages.success(request, f'{product} added to the cart.')
    if action is 'delete':
        cart_item = get_object_or_404(CartItem, id=pk)
        remove_from_cart_with_attr() if cart_item.have_attributes else cart_item.delete()
        messages.warning(request, f'{cart_item} is deleted.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




