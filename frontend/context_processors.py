from catalogue.categories import Category


def frontend(request):
    navbar_categories = Category.browse.navbar()
    return {
        'navbar_categories': navbar_categories
    }