from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from site_settings.models import PaymentMethod
from site_settings.constants import CURRENCY
import uuid


class DefaultOrderModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Friendly ID')
    title = models.CharField(max_length=150, verbose_name='Title')
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    user_account = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    payment_method = models.ForeignKey(PaymentMethod,
                                       null=True,
                                       on_delete=models.PROTECT,
                                       verbose_name='PaymentMethod')
    date_expired = models.DateField(default=timezone.now, verbose_name='Date expired')
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='Value')
    taxes = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='Taxes')
    paid_value = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='Paid Value')
    final_value = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='Final Value')
    discount = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='Discount')
    is_paid = models.BooleanField(default=False, verbose_name='Is Paid')
    printed = models.BooleanField(default=False, verbose_name='Printed')
    objects = models.Manager()

    class Meta:
        abstract = True

    def tag_is_paid(self):
        return 'Is Paid' if self.is_paid else 'Not Paid'

    def tag_value(self):
        return f'{self.value} {CURRENCY}'
    tag_value.short_description = 'Αρχική Αξία'

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'
    tag_final_value.short_description = 'Αξία'

    def tag_paid_value(self):
        return f'{self.paid_value} {CURRENCY}'

    def get_remaining_value(self):
        return self.final_value - self.paid_value


class DefaultOrderItemModel(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    qty = models.PositiveIntegerField(default=1)
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    discount_value = models.IntegerField(default=0, verbose_name='Discount %')
    final_value = models.DecimalField(decimal_places=2, max_digits=20, default=0)

    class Meta:
        abstract = True

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'
    tag_final_value.short_description = 'Αξία'

    def tag_value(self):
        return f'{self.value} {CURRENCY}'
    tag_value.short_description = 'Αρχική Αξία'
