from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from catalogue.models import Product
from .models import OrderItem


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


@staff_member_required
def ajax_order_item(request, action, pk):
    order_item = get_object_or_404(OrderItem, id=pk)
    print(action)
    if action == 'add':
        order_item.qty += 1
    if action == 'remove':
        order_item.qty -= 1 if order_item.qty > 1 else order_item.qty
    order_item.save()
    if action == 'delete':
        order_item.delete()
    instance = order_item.order
    instance.refresh_from_db()
    data = dict()
    data['order_container'] = render_to_string(template_name='point_of_sale/ajax/order_container.html',
                                               request=request,
                                               context={
                                                   'instance': instance
                                               })
    return JsonResponse(data)
