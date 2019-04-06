from string import ascii_letters
from .models import Cart
import random


def generate_cart_id():
    new_id = ''
    for i in range(50):
        new_id = new_id + random.choice(ascii_letters)
    return new_id


def check_if_cart_id(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id is None:
        request.session['cart_id'] = generate_cart_id()
    return request.session['cart_id']


def check_or_create_cart(request):
    user = request.user
    cart_id = check_if_cart_id(request)
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)
    if created and user.is_authenticated:
        cart.user = user
        cart.save()
    return cart


