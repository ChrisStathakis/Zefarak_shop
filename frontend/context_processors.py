from catalogue.categories import Category
from cart.tools import check_or_create_cart


def frontend(request):
    navbar_categories = Category.browse.navbar()
    cart = check_or_create_cart(request)
    return {
        'navbar_categories': navbar_categories,
        'cart': cart
    }