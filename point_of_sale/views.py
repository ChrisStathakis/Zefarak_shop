from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from catalogue.models import Product
from .models import Order, OrderItem
from .forms import OrderCreateForm
from site_settings.models import PaymentMethod

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


@method_decorator(staff_member_required, name='dispatch')
class CreateOrderView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'point_of_sale/form.html'

    def get_initial(self):
        initial = super().get_initial()
        my_qs = PaymentMethod.objects.filter(title='Cash')
        if my_qs.exists():
            initial['payment_method'] = my_qs.first()
        return initial
    
    def get_success_url(self):
        self.new_object.refresh_from_db()
        return reverse('point_of_sale:order_detail', kwargs={'pk': self.new_object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create New Order'
        back_url, delete_url = reverse('point_of_sale:order_list'), None
        context.update(locals())
        return context

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'point_of_sale/order-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.my_query.active()

        context.update(locals())
        return context

    
