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

from .address_models import BillingAddress, ShippingAddress
from .managers import RetailOrderManager, RetailOrderItemManager
from accounts.models import CostumerAccount
from products.models import  Product, SizeAttribute, Gifts
from site_settings.constants import CURRENCY, TAXES_CHOICES
from site_settings.models import DefaultOrderModel, DefaultOrderItemModel
from site_settings.models import PaymentMethod, Shipping, Country
from site_settings.constants import CURRENCY, ORDER_STATUS, ORDER_TYPES, ADDRESS_TYPES
from cart.models import Cart, CartItem, Coupons, CartGiftItem



RETAIL_TRANSCATIONS, PRODUCT_ATTRITUBE_TRANSCATION  = settings.RETAIL_TRANSCATIONS, settings.PRODUCT_ATTRITUBE_TRANSCATION
User = get_user_model()


class Order(DefaultOrderModel):
    number = models.CharField(max_length=128, db_index=True, unique=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='1')
    order_type = models.CharField(max_length=1, choices=ORDER_TYPES, default='r', verbose_name='Είδος Παραστατικού')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                     verbose_name='Συνολικό Κόστος Παραγγελίας')
    user = models.ForeignKey(CostumerAccount,
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
    my_query = RetailOrderManager()
    objects = models.Manager()
    cart_related = models.OneToOneField(Cart, blank=True, null=True, on_delete=models.SET_NULL)
    coupons = models.ManyToManyField(Coupons, blank=True)
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

        super().save(*args, **kwargs)
        if self.costumer_account:
            self.costumer_account.save()

    def update_order(self):
        items = self.order_items.all()
        self.value = items.aggregate(Sum('total_value'))['total_value__sum'] if items else 0
        self.total_cost = items.aggregate(Sum('total_cost_value'))['total_cost_value__sum'] if items else 0

    def check_coupons(self):
        try:
            total_value = 0
            active_coupons = Coupons.my_query.active_date(date=datetime.datetime.now())
            for coupon in self.coupons.all():
                if coupon in active_coupons:
                    if self.value > coupon.cart_total_value:
                        total_value += coupon.discount_value if coupon.discount_value else \
                            (coupon.discount_percent / 100) * self.value if coupon.discount_percent else 0
            self.discount = total_value
        except:
            self.discount = 0

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


