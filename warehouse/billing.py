from django.db import models
from django.db.models import Sum, Q
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete, post_save
from django.shortcuts import reverse
from .abstract_models import DefaultOrderModel
from site_settings.models import Store
from site_settings.constants import CURRENCY
from .managers import BillingManager


class BillCategory(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField( max_length=150)
    balance = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()

    class Meta:
        app_label = 'warehouse'
        verbose_name_plural = '1. Manage Bill Category'
        unique_together = ['store', 'title']

    def __str__(self):
        return f'{self.store} - {self.title}' if self.store else self.title

    def save(self, *args, **kwargs):
        invoices = self.bills.all()
        total_value = invoices.aggregate(Sum('final_value'))['final_value__sum'] if invoices else 0
        paid_value = invoices.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] if \
            invoices.filter(is_paid=True) else 0
        self.balance = total_value - paid_value
        super().save(*args, **kwargs)

    def tag_balance(self):
        return f'{self.balance} {CURRENCY}'
    tag_balance.short_description = 'Balance'

    def get_edit_url(self):
        return reverse('warehouse:bill_category_edit_view', kwargs={'pk':self.id})


class BillInvoice(DefaultOrderModel):
    category = models.ForeignKey(BillCategory, null=True,
                                 on_delete=models.PROTECT,
                                 related_name='bills',
                                 verbose_name='Bill'
                                 )
    objects = models.Manager()
    broswer = BillingManager()

    class Meta:
        app_label = 'warehouse'
        verbose_name_plural = '2. Bill Invoice'
        verbose_name = 'Bill Invoice'
        ordering = ['-date_expired']

    def save(self, *args, **kwargs):
        self.final_value = self.value
        super().save(*args, **kwargs)
        if self.category:
            self.category.save()

    def __str__(self):
        return f'{self.category} - {self.title}' if self.category else f'self.title'

    def tag_category(self):
        return f'{self.category.title}'

    def update_category(self):
        self.category.save()

    def get_edit_url(self):
        return reverse('warehouse:bill_invoice_edit_view', kwargs={'pk': self.id})

    def get_quick_pay_url(self):
        return reverse('warehouse:quick_pay_invoice', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, queryset):
        paid_name = request.GET.getlist('paid_name', None)
        search_name = request.GET.get('search_name', None)
        cate_name = request.GET.getlist('cate_name', None)
        bill_name = request.GET.getlist('bill_name', None)
        date_start, date_end = request.GET.get('date_start', None), request.GET.get('date_end', None)
        if date_start and date_end and date_end > date_start:
            queryset = queryset.filter(date_expired__range=[date_start, date_end])
        queryset = queryset.filter(is_paid=True) if 'paid' in paid_name else queryset.filter(is_paid=False) \
            if 'not_' in paid_name else queryset
        queryset = queryset.filter(category__id__in=cate_name) if cate_name else queryset
        queryset = queryset.filter(category__id__in=bill_name) if bill_name else queryset
        queryset = queryset.filter(Q(title__icontains=search_name) |
                                   Q(category__title__icontains=search_name)
                                   ).distinct() if search_name else queryset
        return queryset


@receiver(post_delete, sender=BillInvoice)
def update_billing(sender, instance, **kwargs):
    if instance.category:
        instance.category.save()
