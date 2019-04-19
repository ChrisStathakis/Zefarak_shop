from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, reverse
from .models import Order
from site_settings.models import PaymentMethod


def create_retail_order_view(request):
    new_order = Order.objects.create(
        payment_method=PaymentMethod.objects.get(id=1)
    )
    return redirect(reverse('point_of_sale:order_detail', kwargs={'pk': new_order.id}))