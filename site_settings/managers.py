from django.db import models


class PaymentMethodManager(models.Manager):

    def active(self):
        return super(PaymentMethodManager, self).filter(active=True)

    def active_for_site(self):
        return super(PaymentMethodManager, self).filter(active=True, site_active=True)

    def check_orders(self):
        return super(PaymentMethodManager, self).filter(is_check=True)


class ShippingManager(models.Manager):

    def active_and_site(self):
        return super(ShippingManager, self).filter(active=True, for_site=True)
