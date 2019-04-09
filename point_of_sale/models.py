from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import F, Sum, Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
import datetime
from decimal import Decimal


from site_settings.constants import CURRENCY, TAXES_CHOICES
from catalogue.models import Product
from catalogue.product_attritubes import Attribute, AttributeClass
from .abstract_models import DefaultOrderModel, DefaultOrderItemModel
from site_settings.models import PaymentMethod, Shipping, Country
from site_settings.constants import CURRENCY, ORDER_STATUS, ORDER_TYPES, ADDRESS_TYPES
from cart.models import Cart, CartItem
from .managers import OrderManager, OrderItemManager
from .address_models import ShippingAddress, BillingAddress

RETAIL_TRANSCATIONS, PRODUCT_ATTRITUBE_TRANSCATION  = settings.RETAIL_TRANSCATIONS, settings.PRODUCT_ATTRITUBE_TRANSCATION
User = get_user_model()


class Order(DefaultOrderModel):
    number = models.CharField(max_length=128, db_index=True, blank=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='1')
    order_type = models.CharField(max_length=1, choices=ORDER_TYPES, default='r', verbose_name='Order Type')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                     verbose_name='Total Cost')
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             verbose_name='Costumer',
                             on_delete=models.SET_NULL,
                             related_name='orders'
                             )

    #  eshop info only
    shipping = models.ForeignKey(Shipping, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='Τρόπος Μεταφοράς')
    shipping_cost = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='Μεταφορικά')
    payment_cost = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='Κόστος Αντικαταβολής')
    day_sent = models.DateTimeField(blank=True, null=True, verbose_name='Ημερομηνία Αποστολής')
    eshop_session_id = models.CharField(max_length=50, blank=True, null=True)
    my_query = OrderManager()
    objects = models.Manager()
    cart_related = models.OneToOneField(Cart, blank=True, null=True, on_delete=models.SET_NULL)
    # coupons = models.ManyToManyField(Coupons, blank=True)
    order_related = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    guest_email = models.EmailField(blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, blank=True, null=True, on_delete=models.SET_NULL)
    billing_address = models.ForeignKey(BillingAddress, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = '1. Orders'
        verbose_name = 'Order'
        ordering = ['-date_expired']

    def __str__(self):
        return self.title if self.title else 'order'

    def save(self, *args, **kwargs):
        order_items = self.order_items.all()
        self.count_items = order_items.count() if order_items else 0
        self.update_order()
        # self.check_coupons()
        # self.update_order()
        self.final_value = self.shipping_cost + self.payment_cost + self.value - self.discount
        self.paid_value = self.paid_value if self.paid_value else 0
        if self.paid_value >= self.final_value: self.is_paid = True
        self.title = f'{self.get_order_type_display()}- 000{self.id}' if not self.title else self.title
        super().save(*args, **kwargs)

    def get_edit_url(self):
        return reverse('point_of_sale:order_detail', kwargs={'pk': self.id })

    def update_order(self):
        items = self.order_items.all()
        self.value = items.aggregate(Sum('total_value'))['total_value__sum'] if items else 0
        self.total_cost = items.aggregate(Sum('total_cost_value'))['total_cost_value__sum'] if items else 0

    def tag_value(self):
        return '%s %s' % (self.value, CURRENCY)

    def tag_final_value(self):
        return '%s %s' % (self.final_value, CURRENCY)

    tag_final_value.short_description = 'Value'

    def tag_paid_value(self):
        return '%s %s' % (self.paid_value, CURRENCY)

    tag_paid_value.short_description = 'Αποπληρωμένο Πόσο'

    def tag_cost_value(self):
        return '%s %s' % (self.total_cost, CURRENCY)

    def tag_discount(self):
        return '%s %s' % (self.discount, CURRENCY)

    @property
    def get_total_taxes(self):
        choice = 24
        for ele in TAXES_CHOICES:
            if ele[0] == self.taxes:
                choice = ele[1]
        return self.final_value * (Decimal(choice) / 100)

    @property
    def get_order_items(self):
        return self.order_items.all()

    @property
    def tag_remain_value(self):
        return '%s %s' % (round(self.final_value - self.paid_value, 2), CURRENCY)

    def tag_status(self):
        return f'{self.get_status_display()}'

    def tag_order_type_and_status(self):
        text = f'{self.get_order_type_display()} - {self.get_status_display()}' if self.order_type in ['e',
                                                                                                       'r'] else f'{self.get_order_type_display()}'
        back_color = 'success' if self.order_type in ['e', 'r'] and self.status in ['4', '7',
                                                                                    '8'] else 'info' if self.order_type in [
            'e', 'r'] else 'danger' if self.order_type == 'c' else 'warning'
        return mark_safe('<td class="%s">%s</td>' % (back_color, text))

    def tag_costumer(self):
        return self.costumer_account

    def tag_seller_point(self):
        return self.seller_account.username if self.seller_account else 'No data'

    def is_printed(self):
        return 'Printed' if self.printed else 'Not Printed'

    @staticmethod
    def create_eshop_order(request, form, cart):
        email = form.cleaned_data.get('email', 'admin@gmail.gr')
        shipping = form.cleaned_data.get('Shipping', Shipping.objects.first())
        payment_method = form.cleaned_data.get('payment_method', PaymentMethod.objects.first())
        user = request.user if request.user.is_authenticated else None
        new_order = Order.objects.create(
            cart_related=cart,
            order_type='e',
            shipping=shipping,
            payment_method=payment_method,
            guest_email=email
        )
        if user:
            new_order.user = user
        new_order.save()
        for item in cart.cart_items.all():
            new_item = OrderItem.objects.create(
                order=new_order,
                title=item.product,
                qty=item.qty,
            )
        return new_order

    @staticmethod
    def eshop_orders_filtering(request, queryset):
        search_name = request.GET.get('search_name', None)
        paid_name = request.GET.getlist('paid_name', None)
        printed_name = request.GET.get('printed_name', None)
        status_name = request.GET.getlist('status_name', None)
        payment_name = request.GET.getlist('payment_name', None)
        sell_point_name = request.GET.getlist('sell_point_name', None)
        queryset = queryset.filter(printed=False) if printed_name else queryset
        queryset = queryset.filter(payment_method__id__in=payment_name) if payment_name else queryset
        queryset = queryset.filter(status__in=status_name) if status_name else queryset
        queryset = queryset.filter(is_paid=False) if paid_name else queryset
        queryset = queryset.filter(Q(title__icontains=search_name) |
                                   Q(cellphone__icontains=search_name) |
                                   Q(address__icontains=search_name) |
                                   Q(city__icontains=search_name) |
                                   Q(zip_code__icontains=search_name) |
                                   Q(phone__icontains=search_name) |
                                   Q(first_name__icontains=search_name) |
                                   Q(last_name__icontains=search_name)
                                   ).distinct() if search_name else queryset
        queryset = queryset.filter(seller_account__id__in=sell_point_name) if sell_point_name else queryset
        return queryset


@receiver(post_save, sender=Order)
def create_unique_number(sender, instance, **kwargs):
    if not instance.number:
        MAX_NUMBERS = 8
        len_num = len(str(instance.id))
        filling_len = MAX_NUMBERS-len_num
        instance.number = filling_len*'0'+ str(instance.id)
        instance.save()


class OrderItem(DefaultOrderItemModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    title = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='retail_items')
    #  warehouse_management
    is_find = models.BooleanField(default=False)
    is_return = models.BooleanField(default=False)
    attribute = models.BooleanField(default=False)
    total_value = models.DecimalField(max_digits=20, decimal_places=0, default=0, help_text='qty*final_value')
    total_cost_value = models.DecimalField(max_digits=20, decimal_places=0, default=0, help_text='qty*cost')
    broswer = OrderItemManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = '2. Προϊόντα Πωληθέντα'
        ordering = ['-order__timestamp', ]
        unique_together = ['title', 'order']

    def __str__(self):
        return self.title.title if self.title else 'Something is wrong'

    def save(self, *args, **kwargs):
        self.value = self.title.price if self.title else 0
        self.discount_value = self.title.price_discount if self.title else 0
        self.cost = self.title.price_buy if self.title else 0
        self.final_value = self.discount_value if self.discount_value > 0 else self.value
        self.total_value = self.final_value * self.qty
        self.total_cost_value = self.cost * self.qty
        if self.attribute:
            attributes = self.attributes.all()
            self.qty = attributes.aggregate(Sum('qty'))['qty__sum'] if attributes.exists() else 0
        super().save(*args, **kwargs)
        self.title.save()
        self.order.save()

    def update_warehouse(self, transcation_type, qty):
        update_warehouse(self, transcation_type, qty)

    def update_order(self):
        self.order.save()

    def get_clean_value(self):
        return self.final_value * (100 - self.order.taxes / 100)

    @property
    def get_total_value(self):
        return round(self.final_value * self.qty, 2)

    @property
    def get_total_cost_value(self):
        return round(self.cost * self.qty, 2)

    def tag_clean_value(self):
        return '%s %s' % (self.get_clean_value(), CURRENCY)

    def tag_total_value(self):
        return '%s %s' % (self.get_total_value, CURRENCY)

    tag_total_value.short_description = 'Συνολική Αξία'

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'

    tag_final_value.short_description = 'Αξία Μονάδας'

    def tag_value(self):
        return '%s %s' % (self.value, CURRENCY)

    def tag_found(self):
        return 'Found' if self.is_find else 'Not Found'

    def tag_total_taxes(self):
        return '%s %s' % (round(self.value * self.qty * (Decimal(self.order.taxes) / 100), 2), CURRENCY)

    def type_of_order(self):
        return self.order.order_type

    def template_tag_total_price(self):
        return "{0:.2f}".format(round(self.value * self.qty, 2)) + ' %s' % (CURRENCY)

    def price_for_vendor_page(self):
        #  returns silimar def for price in vendor_id page
        return self.value

    def absolute_url_vendor_page(self):
        return reverse('retail_order_section', kwargs={'dk': self.order.id})

    @staticmethod
    def create_or_edit_item(order, product, qty, transation_type):
        instance, created = OrderItem.objects.get_or_create(order=order, title=product)
        if transation_type == 'ADD':
            if not created:
                instance.qty += qty
            else:
                instance.qty = qty
                instance.value = product.price
                instance.discount_value = product.price_discount
                instance.cost = product.price_buy
        if transation_type == 'REMOVE':
            instance.qty -= qty
            instance.qty = 1 if instance.qty <= 0 else instance.qty
        instance.save()
        if transation_type == 'DELETE':
            instance.delete()
        order.save()


def create_destroy_title():
    last_order = OrderItem.objects.all().last()
    if last_order:
        number = int(last_order.id) + 1
        return 'ΚΑΤ' + str(number)
    else:
        return 'ΚΑΤ1'


@receiver(post_delete, sender=OrderItem)
def update_warehouse(sender, instance, **kwargs):
    instance.title.save()


class OrderItemAttribute(models.Model):
    attr_class = models.ForeignKey(AttributeClass, null=True, on_delete=models.SET_NULL)
    title = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='attributes')
    qty = models.DecimalField(default=1, decimal_places=2, max_digits=10)

    def __str__(self):
        return f'{self.title} - {self.order_item}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order_item.save()


class OrderProfile(models.Model):
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT)
    cellphone = models.CharField(max_length=10)
    phone = models.CharField(max_length=10, blank=True)
    notes = models.TextField()
    order_type = models.CharField(max_length=50, choices=ADDRESS_TYPES,)
    order_related = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_profiles')

    class Meta:
        unique_together = ['order_related', 'order_type']

    def tag_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def tag_full_address(self):
        return f'{self.address} {self.city} TK..{self.zip_code}'

    def tag_phones(self):
        return f'{self.cellphone} ,{self.phone}'

    @staticmethod
    def create_profile_from_cart(form, order, type='shipping'):
        billing_profile, created = Order.objects.get_or_create(order_related=order, order_type=type)
        billing_profile.email = form.cleaned_data.get('email', 'Error')
        billing_profile.first_name = form.cleaned_data.get('first_name', 'Error')
        billing_profile.last_name = form.cleaned_data.get('last_name', 'Error')
        billing_profile.cellphone = form.cleaned_data.get('cellphone', 'Error')
        billing_profile.zip_code = form.cleaned_data.get('postcode', 'Error')
        billing_profile.address = form.cleaned_data.get('address', 'Error')
        billing_profile.city = form.cleaned_data.get('city', 'Error')
        billing_profile.phone = form.cleaned_data.get('phone', None)
        billing_profile.notes = form.cleaned_data.get('notes', None)
        billing_profile.save()
