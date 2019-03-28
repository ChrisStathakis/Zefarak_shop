from django.db import models


class ShippingAddress(models.Model):
    title = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    first_name = models.CharField(blank=True, null=True, max_length=150, verbose_name='First Name')
    last_name = models.CharField(blank=True, null=True, max_length=150, verbose_name='Last Name')
    #  shipping_information
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Address')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='City')
    zip_code = models.IntegerField(blank=True, null=True, verbose_name='Postal')
    #  personal stuff
    phone = models.CharField(max_length=10, blank=True, verbose_name="Phone")
    cellphone = models.CharField(max_length=10, blank=True, verbose_name='Cell Phone')
    #  if costumer is not Retail

    def __str__(self):
        return self.title if self.title else f'{self.first_name} {self.last_name}'


class BillingAddress(models.Model):
    first_name = models.CharField(blank=True, null=True, max_length=150, verbose_name='First Name')
    last_name = models.CharField(blank=True, null=True, max_length=150, verbose_name='Last Name')
    #  shipping_information
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Address')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='City')
    zip_code = models.IntegerField(blank=True, null=True, verbose_name='Postal')
    #  personal stuff
    phone = models.CharField(max_length=10, blank=True, verbose_name="Phone")
    cellphone = models.CharField(max_length=10, blank=True, verbose_name='Cell Phone')

    need_invoice = models.BooleanField(default=False)
    is_retail = models.BooleanField(default=True)
    is_eshop = models.BooleanField(default=True)
    vat = models.CharField(max_length=9, blank=True, verbose_name="ΑΦΜ")
    vat_city = models.CharField(max_length=100, blank=True, null=True)
    company_detail = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return  f'Billing Address {self.first_name} {self.last_name}'
