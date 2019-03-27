from django.db import models
import datetime


class GenericQueryset(models.QuerySet):

    def until_today(self):
        return self.filter(date_expired__lte=datetime.datetime.today())

    def not_paid(self):
        return self.filter(is_paid=False)

    def invoices_per_store(self, store):
        return self.filter(category__store=store)

    def until_today_not_paid(self):
        return self.filter(is_paid=False, date_expired__lte=datetime.datetime.today())

    def until_next_ten_days_not_paid(self):
        return self.filter(is_paid=False, date_expired__lte=datetime.datetime.today()+datetime.timedelta(days=10))


class BillingManager(models.Manager):

    def get_queryset(self):
        return GenericQueryset(self.model, using=self._db)


class PayrollManager(models.Manager):

    def get_queryset(self):
        return GenericQueryset(self.model, using=self._db)
