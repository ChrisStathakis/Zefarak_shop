from django.views.generic import TemplateView, ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required


from .models import Order, OrderItem


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'point_of_sale/dashboard.html'


@method_decorator(staff_member_required, name='dispatch')
class OrderListView(ListView):
    template_name = 'point_of_sale/order-list.html'
    model = Order
    paginate_by = 50

    def get_queryset(self):
        queryset = Order.objects.all()

        return queryset


@method_decorator(staff_member_required)
class CreateOrderView(CreateView):
    model = Order
    form = ''
    template_name = ''