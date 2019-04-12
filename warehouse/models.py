from django.db import models
from catalogue.product_details import Vendor
from .payroll import *
from .billing import *
from .abstract_models import DefaultOrderModel


class Invoice(DefaultOrderModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor_orders')
    total_discount = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    clean_value = models.DecimalField(default=0.00, max_digits=15, decimal_places=2,)
    taxes_modifier = models.CharField(max_length=1, choices=TAXES_CHOICES, default='3')
    taxes = models.DecimalField(default=0.00, max_digits=15, decimal_places=2,)
    order_type = models.CharField(default=1, max_length=1, choices=WAREHOUSE_ORDER_TYPE)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "1. Warehouse Invoice"
        ordering = ['-date_expired']

    def __str__(self):
        return self.title

    @staticmethod
    def filter_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        vendor_name = request.GET.getlist('vendor_name', None)
        balance_name = request.GET.get('balance_name', None)
        paid_name = request.GET.get('is_paid_name', None)
        # date_start, date_end, date_range, months_list = estimate_date_start_end_and_months(request)
        payment_name = request.GET.getlist('payment_name', None)
        order_type_name = request.GET.getlist('order_type_name', None)
        try:
            queryset = queryset.filter(order_type__in=order_type_name) if order_type_name else queryset
            queryset = queryset.filter(vendor__id__in=vendor_name) if vendor_name else queryset
            queryset = queryset.filter(Q(title__icontains=search_name) |
                                       Q(vendor__title__icontains=search_name)
                                       ).dinstict() if search_name else queryset
            queryset = queryset.filter(date_expired__range=[date_start, date_end]) if date_start else queryset
            queryset = queryset.filter(is_paid=True) if paid_name == 'paid' else queryset.filter(is_paid=False) \
                if paid_name == 'not_paid' else queryset
            queryset = queryset.filter(total_price__gte=balance_name) if balance_name else queryset
            queryset = queryset.filter(payment_name__id__in=payment_name) if payment_name else queryset
        except:
            queryset = queryset
        return queryset



