from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from .tools import check_or_create_cart
# Create your views here.
from catalogue.models import Product
from .models import CartItem


def add_to_cart(request, pk):
    cart = check_or_create_cart(request)
    product = get_object_or_404(Product, id=pk)
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if created:
        cart_item.qty = 1
        cart_item.value = product.price
        cart_item.price_discount = product.price_discount
    else:
        cart_item.qty += 1
    cart_item.save()
    messages.success(request, f'{product} added to the cart.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, id=pk)
    cart_item.delete()
    messages.success(request, f'{cart_item} is deleted.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))