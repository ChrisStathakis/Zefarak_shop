from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.shortcuts import reverse, get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from catalogue.models import Product
from catalogue.product_attritubes import Attribute
from .models import Order, OrderItem, OrderItemAttribute
from .forms import OrderCreateForm, OrderItemCreateForm, OrderItemAttrForm
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
class EshopListView(ListView):
    template_name = 'point_of_sale/order-list.html'
    model = Order
    paginate_by = 30

    def get_queryset(self):
        queryset = Order.my_query.get_queryset().eshop_orders()
        queryset = Order.eshop_orders_filtering(self.request, queryset)
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
        instance = self.object
        context.update(locals())
        return context


@staff_member_required
def check_product(request, pk, dk):
    instance = get_object_or_404(Product, id=dk)
    if instance.product_class.have_attribute:
        return redirect(reverse('point_of_sale:add_product_attr', kwargs={'pk': pk, 'dk': dk}))
    else:
        return redirect(reverse('point_of_sale:add_product', kwargs={'pk': pk, 'dk': dk}))


@staff_member_required
def order_add_product(request, pk, dk):
    instance = get_object_or_404(Product, id=dk)
    order = get_object_or_404(Order, id=pk)
    order_item, created = OrderItem.objects.get_or_create(title=instance, order=order)
    order_item.qty = 1 if created else order_item.qty + 1
    if created:
        order_item.value = instance.price
        order_item.discount_value = instance.price_discount
        order_item.cost = instance.price_buy
    order_item.save()
    return redirect(reverse('point_of_sale:order_detail', kwargs={'pk': pk}))


@staff_member_required
def order_add_product_with_attr(request, pk, dk):
    instance = get_object_or_404(Product, id=dk)
    order = get_object_or_404(Order, id=pk)
    get_attr = instance.attr_class.filter(class_related__have_transcations=True)
    all_attrs = Attribute.objects.filter(class_related=get_attr.first()) if get_attr.exists() else Attribute.objects.none()
    back_url = reverse('point_of_sale:order_detail', kwargs={'pk': pk})
    return render(request, 'point_of_sale/add_to_order_with_attr.html', context=locals())


@staff_member_required
def add_to_order_with_attr(request, pk, dk, lk):
    instance = get_object_or_404(Product, id=dk)
    order = get_object_or_404(Order, id=pk)
    attribute = get_object_or_404(Attribute, id=lk)
    order_item, i_created = OrderItem.objects.get_or_create(title=instance, order=order)
    order_item_attr, created = OrderItemAttribute.objects.get_or_create(order_item=order_item,
                                                                        title=attribute
                                                                        )
    order_item_attr.qty = 1 if created else order_item_attr.qty+1
    order_item_attr.save()
    return redirect(reverse('point_of_sale:order_detail', kwargs={'pk': pk}))


@staff_member_required
def order_item_edit_with_attr(request, pk):
    instance = get_object_or_404(OrderItem, id=pk)
    product = instance.title
    selected_attr = instance.attributes.all()
    return render(request, 'point_of_sale/order-item-edit.html', context=locals())

