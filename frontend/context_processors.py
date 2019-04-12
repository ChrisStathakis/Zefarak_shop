from catalogue.categories import Category
from cart.tools import check_or_create_cart
from accounts.forms import LoginForm


def frontend(request):
    navbar_categories = Category.browse.navbar()
    cart = check_or_create_cart(request)
    login_form = LoginForm()
    return {
        'navbar_categories': navbar_categories,
        'cart': cart,
        'login_form': login_form
    }