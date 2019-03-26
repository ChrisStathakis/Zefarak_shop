from django.db import models


class GenericQueryset(models.QuerySet):

    def not_paid(self):
        return self.filter(is_paid=False)

    def invoices_per_store(self, store):
        return self.filter(category__store=store)


class BillingManager(models.Manager):

    def get_queryset(self):
        return GenericQueryset(self.model, using=self._db)


class PayrollManager(models.Manager):

    def get_queryset(self):
        return GenericQueryset(self.model, using=self._db)
