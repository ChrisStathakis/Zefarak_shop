from django.db import models
from datetime import datetime


class RetailQuerySet(models.QuerySet):

    def sells(self, date_start=None, date_end=None):
        if date_start and date_end:
            return self.filter(order_type__in=['r', 'e'],
                               date_expired__range=[date_start, date_end]
                               )
        return self.filter(order_type__in=['r', 'e'])

    def eshop_orders(self, date_start=None, date_end=None):
        return self.sells(date_start, date_end).filter(order_type='e')

    def today_sells(self):
        return self.sells().filter(date_expired=datetime.now())

    def returns(self, date_start, date_end):
        return self.filter(order_type='b',
                           date_expired__range=[date_start, date_end]
                           )

    def export_invoices(self, date_start, date_end):
        return self.filter(order_type='wr',
                           date_expired__range=[date_start, date_end]
                           )

    def sells_by_date_range(self, date_start, date_end):
        return self.sells().filter(date_expired__range=[date_start, date_end])

    def all_by_date_range(self, date_start, date_end):
        return self.filter(date_expired__range=[date_start, date_end])


class OrderManager(models.Manager):

    def get_queryset(self):
        return RetailQuerySet(self.model, using=self._db)


class OrderItemManager(models.Manager):
    pass
