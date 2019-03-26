from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete, post_save
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings



from site_settings.constants import *
from site_settings.models import PaymentMethod, Store
from .managers import PayrollManager


import datetime
from django.db import models
from django.db.models import Sum, Q
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete, post_save

from .abstract_models import DefaultOrderModel
from site_settings.models import Store

User = get_user_model()
CURRENCY = settings.CURRENCY


class Occupation(models.Model):
    store = models.ManyToManyField(Store, null=True, blank=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=64, verbose_name='Occupation')
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0, verbose_name='Balance')

    objects = models.Manager()

    class Meta:
        app_label = 'warehouse'
        verbose_name_plural = "3. Occupations"
        verbose_name = 'Occupation'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.balance = self.employees.all().aggregate(Sum('balance'))['balance__sum'] \
            if self.employees.exists() else 0
        super().save(*args, *kwargs)

    def tag_balance(self):
        return '%s %s' % (self.balance, CURRENCY)
    tag_balance.short_description = 'Balance'

    def get_edit_url(self):
        return reverse('warehouse:occupation_edit', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        queryset = queryset.filter(title__icontains=search_name) if search_name else queryset
        return queryset


class Employee(models.Model):
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=64, unique=True, verbose_name='Name')
    phone = models.CharField(max_length=10, verbose_name='Phone', blank=True)
    phone1 = models.CharField(max_length=10, verbose_name='Cell Phone', blank=True)
    date_started = models.DateField(default=timezone.now, verbose_name='Date started')
    occupation = models.ForeignKey(Occupation, null=True, verbose_name='Occupation', on_delete=models.PROTECT, related_name='employees')
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0, verbose_name='Balance')
    vacation_days = models.IntegerField(default=0, verbose_name='Remaining Vacation Days')

    objects = models.Manager()

    class Meta:
        app_label = 'warehouse'
        verbose_name_plural = "4. Employee"
        verbose_name = 'Υπάλληλος'

    def save(self, *args, **kwargs):
        self.balance = self.update_balance()
        super().save(*args, **kwargs)
        self.occupation.save() if self.occupation else ''

    def update_balance(self):
        queryset = self.person_invoices.all()
        value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.aggregate(Sum('paid_value'))['paid_value__sum'] if queryset else 0
        diff = value - paid_value
        return diff

    def __str__(self):
        return self.title

    def tag_balance(self):
        return '%s %s' % (self.balance, CURRENCY)

    def tag_occupation(self):
        return f'{self.occupation.title}'

    def get_edit_url(self):
        return reverse('warehouse:payroll_employee_edit', kwargs={'pk': self.id})

    def get_payroll_create_url(self):
        return reverse('warehouse:employee_create_payroll', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        occup_name = request.GET.getlist('occup_name', None)
        queryset = queryset.filter(title__icontains=search_name) if search_name else queryset
        queryset = queryset.filter(occupation__id__in=occup_name) if occup_name else queryset
        return queryset


class Payroll(DefaultOrderModel):
    employee = models.ForeignKey(Employee, verbose_name='Employee', on_delete=models.PROTECT,
                               related_name='person_invoices')
    category = models.CharField(max_length=1, choices=PAYROLL_CHOICES, default='1')
    objects = models.Manager()
    browser = PayrollManager()

    class Meta:
        app_label = 'warehouse'
        verbose_name_plural = '2. Μισθόδοσία'
        verbose_name = 'Εντολή Πληρωμής'
        ordering = ['is_paid', '-date_expired', ]

    def __str__(self):
        return '%s %s' % (self.date_expired, self.employee.title)

    def save(self, *args, **kwargs):
        self.final_value = self.value
        self.paid_value = self.final_value if self.is_paid else 0
        super(Payroll, self).save(*args, **kwargs)
        self.employee.save()

    def tag_model(self):
        return f'Payroll - {self.employee.title}'

    def tag_person(self):
        return f'{self.employee.title}'

    def update_category(self):
        self.employee.update_balance()

    def tag_value(self):
        return '%s %s' % (self.value, CURRENCY)

    tag_value.short_description = 'Αξία Παραστατικού'

    def tag_is_paid(self):
        return "Is Paid" if self.is_paid else "Not Paid"

    def get_remaining_value(self):
        return self.final_value - self.paid_value

    def tag_remaining_value(self):
        return '%s %s' % (self.get_remaining_value(), CURRENCY)

    @staticmethod
    def filters_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        person_name = request.GET.getlist('person_name', None)
        occup_name = request.GET.getlist('cate_name', None)
        paid_name = request.GET.getlist('paid_name', None)
        date_start, date_end = request.GET.get('date_start', None), request.GET.get('date_end', None)

        if date_start and date_end and date_end > date_start:
            queryset = queryset.filter(date_expired__range=[date_start, date_end])
        queryset = queryset.filter(is_paid=True) if 'paid' in paid_name else queryset.filter(is_paid=False) \
            if 'not_paid' in paid_name else queryset
        queryset = queryset.filter(person__id__in=person_name) if person_name else queryset
        queryset = queryset.filter(person__occupation__id__in=occup_name) if occup_name else queryset
        queryset = queryset.filter(Q(title__icontains=search_name) |
                                   Q(person__title__icontains=search_name) |
                                   Q(person__occupation__title__icontains=search_name)
                                   ).distict() if search_name else queryset

        return queryset


@receiver(pre_delete, sender=Payroll)
def update_on_delete_payrolls(sender, instance, *args, **kwargs):
    get_orders = instance.payment_orders.all()
    for order in get_orders:
        order.delete()


@receiver(post_delete, sender=Payroll)
def update_person_on_delete(sender, instance, *args, **kwargs):
    person = instance.person
    person.balance -= instance.final_value - instance.paid_value
    person.save()
