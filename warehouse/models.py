from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import messages
from catalogue.product_details import Vendor, VendorPaycheck
from .payroll import *
from .billing import *
from .abstract_models import DefaultOrderModel, DefaultOrderItemModel
from catalogue.models import Product
from site_settings.tools import estimate_date_start_end_and_months
from decimal import Decimal


def upload_image(instance, filename):
    return f'warehouse_images/{instance.order_related.vendor.title}/{instance.order_related.title}/{filename}'


def validate_file(value):
    if value.file.size > 1024*1024*5:
        return ValidationError('This file is biger than 5 mb')


class Invoice(DefaultOrderModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor_orders')
    additional_value = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    clean_value = models.DecimalField(default=0.00, max_digits=15, decimal_places=2,)
    taxes_modifier = models.CharField(max_length=1, choices=TAXES_CHOICES, default='1')
    taxes = models.DecimalField(default=0.00, max_digits=15, decimal_places=2,)
    order_type = models.CharField(default=1, max_length=1, choices=WAREHOUSE_ORDER_TYPE)
    paycheck = models.ManyToManyField(VendorPaycheck)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "1. Warehouse Invoice"
        ordering = ['-date_expired']

    def save(self, *args, **kwargs):
        order_items = self.order_items.all()
        if order_items.exists():
            self.clean_value = order_items.aggregate(Sum('total_clean_value'))['total_clean_value__sum']
            self.taxes = Decimal(self.clean_value) * Decimal((self.get_taxes_modifier_display())/100)

        else:
            self.clean_value, self.taxes, self.final_value = 0, 0, 0
        self.final_value = self.clean_value + self.taxes + self.additional_value
        self.paid_value = self.final_value if self.is_paid else self.paid_value
        super().save(*args, **kwargs)
        self.vendor.update_output_value()

    def __str__(self):
        return self.title

    def tag_discount(self):
        return f'{self.discount} %'

    def tag_clean_value(self):
        return f'{self.clean_value} {CURRENCY}'

    def tag_taxes(self):
        return f'{self.taxes} {CURRENCY}'

    def tag_additional_value(self):
        if self.additional_value >= 0:
            return f'Added {self.additional_value}'
        return f'Removed {self.additional_value}'

    def get_edit_url(self):
        return reverse('warehouse:update_order', kwargs={'pk': self.id})

    @staticmethod
    def filter_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        vendor_name = request.GET.getlist('vendor_name', None)
        paid_name = request.GET.get('paid_name', None)
        date_start, date_end, date_range, months_list = estimate_date_start_end_and_months(request)
        payment_name = request.GET.getlist('payment_name', None)
        order_type_name = request.GET.getlist('order_type_name', None)
        try:
            queryset = queryset.filter(order_type__in=order_type_name) if order_type_name else queryset
            queryset = queryset.filter(vendor__id__in=vendor_name) if vendor_name else queryset
            queryset = queryset.filter(Q(title__contains=search_name) |
                                       Q(vendor__title__contains=search_name)
                                       ).dinstict() if search_name else queryset
            queryset = queryset.filter(date_expired__range=[date_start, date_end]) if date_start else queryset
            queryset = queryset.filter(is_paid=True) if paid_name == '1' else queryset.filter(is_paid=False) \
                if paid_name == '2' else queryset
            queryset = queryset.filter(payment_name__id__in=payment_name) if payment_name else queryset
        except:
            queryset = queryset
        return queryset


class InvoiceImage(models.Model):
    order_related = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='images')
    file = models.FileField(upload_to=upload_image, null=True, validators=[validate_file, ])
    is_first = models.BooleanField(default=True)

    def __str__(self):
        return '%s-%s' % (self.order_related.title, self.id)

    def get_edit_url(self):
        return reverse('warehouse:update-order-image', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('warehouse:delete-order-image', kwargs={'pk': self.id})


class InvoiceOrderItem(DefaultOrderItemModel):
    sku = models.CharField(max_length=150, null=True)
    order = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='invoice_products'
                                )
    unit = models.CharField(max_length=1, choices=UNIT, default='1')
    total_clean_value = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    total_final_value = models.DecimalField(default=0, max_digits=14, decimal_places=2)

    class Meta:
        unique_together = ['order', 'product']

    def __str__(self):
        return f'{self.product}'

    def save(self, *args, **kwargs):
        self.final_value = Decimal(self.value) * (100 - self.discount_value) / 100
        print(self.value, self.final_value)
        self.total_clean_value = Decimal(self.final_value) * Decimal(self.qty)
        self.total_final_value = Decimal(self.total_clean_value) * Decimal((100 + self.order.get_taxes_modifier_display()) / 100)
        super().save(*args, **kwargs)
        self.product.price_buy = self.value
        self.product.order_discount = self.discount_value
        self.product.save()
        self.order.save()

    def get_edit_url(self):
        return reverse('warehouse:order-item-update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('warehouse:order-item-delete', kwargs={'pk': self.id})

    def remove_from_order(self, qty):
        if WAREHOUSE_ORDERS_TRANSCATIONS:
            product = self.product
            product.qty -= qty
            product.save()
        self.order.save()

    def quick_add_to_order(self, qty):
        qty = Decimal(qty) if qty else 0
        if WAREHOUSE_ORDERS_TRANSCATIONS:
            product = self.product
            product.qty += qty
            product.save()

    def tag_discount(self):
        return f'{self.discount_value} %'

    def tag_total_clean_value(self):
        return f'{self.total_clean_value} {CURRENCY}'

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'

    def tag_total_final_value(self):
        return '%s %s' % (round(self.total_value_with_taxes), CURRENCY)

    def tag_total_taxes(self):
        taxes = self.total_value_with_taxes - self.total_clean_value
        return f'{taxes} {CURRENCY}'

    def tag_order(self):
        return f"{self.order.title} - {self.order.vendor.title}"
    tag_order.short_description = 'Παραστατικό'

    def tag_product(self):
        return f'{self.product.title}'
    tag_product.short_description = 'Προϊόν'

    @staticmethod
    def filters_data(request, queryset):
        category_name = request.GET.getlist('category_name', None)
        brand_name = request.GET.getlist('brand_name', None)
        vendor_name = request.GET.getlist('vendor_name', None)
        queryset = queryset.filter(product__category__id__in=category_name) if category_name else queryset
        queryset = queryset.filter(product__brand__id__in=brand_name) if brand_name else queryset
        queryset = queryset.filter(product__vendor__id__in=vendor_name) if vendor_name else queryset
        return queryset


@receiver(post_delete, sender=InvoiceOrderItem)
def update_qty_on_delete(sender, instance, *args, **kwargs):
    product, order, self = instance.product, instance.order, instance
    product.save() if WAREHOUSE_ORDERS_TRANSCATIONS else ''
    self.order.save()

