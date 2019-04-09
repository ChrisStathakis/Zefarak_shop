from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from catalogue.models import Product
from .models import CartItem, Cart
from .tools import add_to_cart, add_to_cart_with_attr, remove_from_cart_with_attr


class CartListView(ListView):
    model = Cart
    template_name = 'cart/listview.html'

    def get_queryset(self):
        queryset = Cart.objects.all()

        return queryset


class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        back_url = self.request.GET.get('back_url', reverse('cart:cart_list'))
        context.update(locals())
        return context


def check_cart_movement(request, pk, action):
    if action == 'add':
        product = get_object_or_404(Product, id=pk)
        add_to_cart_with_attr() if product.have_attr else add_to_cart(request, product)
        messages.success(request, f'{product} added to the cart.')
    if action == 'remove':
        cart_item = get_object_or_404(CartItem, id=pk)
        remove_from_cart_with_attr() if cart_item.have_attributes else cart_item.delete()
        messages.warning(request, f'{cart_item} is deleted.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def ajax_cart_change_qty(request, pk):
    instance = get_object_or_404(CartItem, id=pk)
    new_qty = request.GET.get('qty', 1)
    new_qty = int(new_qty)
    instance.qty = new_qty
    instance.save()
    instance.refresh_from_db()
    cart = instance.cart
    cart.refresh_from_db()
    data = dict()
    data['result'] = render_to_string(template_name='cart/ajax_cart_container.html',
                                      request=request,
                                      context={'cart': cart})
    return JsonResponse(data)
