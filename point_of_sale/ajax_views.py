from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import JsonResponse


from catalogue.models import Product


@staff_member_required
def ajax_search_products(request):
    products = Product.my_query.active()
    products = Product.filters_data(request, products)
    data = dict()
    data['products_container'] = render_to_string(template_name='point_of_sale/ajax/products_container.html',
                                                  request=request,
                                                  context={'products': products}
                                                  )
    return JsonResponse(data)
