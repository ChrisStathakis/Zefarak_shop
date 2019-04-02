from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from site_settings.abstract_models import DefaultBasicModel
from site_settings.constants import CURRENCY
from .models import Product
from .managers import AttributeManager


class Characteristics(DefaultBasicModel):
    title = models.CharField(max_length=120, unique=True)

    class Meta:
        app_label = 'catalogue'

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('dashboard:char_edit_view', kwargs={'pk': self.id})


class CharacteristicsValue(DefaultBasicModel):
    title = models.CharField(max_length=120, unique=True)
    char_related = models.ForeignKey(Characteristics, on_delete=models.SET_NULL, null=True, related_name='my_values')
    custom_ordering = models.IntegerField(default=0, verbose_name='Ordering', help_text='Bigger is better')

    class Meta:
        app_label = 'catalogue'
        ordering = ['-custom_ordering', 'title']

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('dashboard:char_value_edit_view', kwargs={'pk': self.id})


class ProductCharacteristics(models.Model):
    product_related = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    title = models.ForeignKey(Characteristics, on_delete=models.CASCADE)
    value = models.ForeignKey(CharacteristicsValue, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        app_label = 'catalogue'
        unique_together = ('product_related', 'title')

    def __str__(self):
        return f'{self.title.title} - {self.value.title}'


class AttributeClass(models.Model):
    title = models.CharField(unique=True, max_length=150)
    have_transcations = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('dashboard:attribute_class_edit_view', kwargs={'pk': self.id})


class AttributeTitle(models.Model):
    title = models.CharField(max_length=150)
    attri_by = models.ForeignKey(AttributeClass, null=True, on_delete=models.CASCADE, related_name='my_values')
    ordering_by = models.IntegerField(default=0, help_text='Bigger is first')

    class Meta:
        unique_together = ['title', 'attri_by']
        ordering = ['-ordering_by', 'title']
        app_label = 'catalogue'

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('dashboard:attribute_title_edit_view', kwargs={'pk': self.id})


class AttributeProductClass(models.Model):
    class_related = models.ForeignKey(AttributeClass, on_delete=models.CASCADE)
    product_related = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, verbose_name='Προϊόν',
                                        related_name='attr_class')

    class Meta:
        unique_together = ['class_related', 'product_related']


class Attribute(models.Model):
    title = models.ForeignKey(AttributeTitle, on_delete=models.CASCADE, related_name='sizes')
    class_related = models.ForeignKey(AttributeProductClass, on_delete=models.CASCADE, related_name='my_attributes')
    product_related = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, verbose_name='Προϊόν',
                                        related_name='attributes')
    qty = models.DecimalField(default=0, decimal_places=2, max_digits=6, verbose_name='Ποσότητα')
    order_discount = models.IntegerField(null=True, blank=True, default=0, verbose_name="'Εκπτωση Τιμολογίου σε %")
    price_buy = models.DecimalField(decimal_places=2, max_digits=6, default=0, verbose_name="Τιμή Αγοράς")
    my_query = AttributeManager()
    objects = models.Manager()

    class Meta:
        app_label = 'catalogue'
        verbose_name_plural = '2. Μεγεθολόγιο'
        unique_together = ['title', 'product_related']
        ordering = ['title']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product_related.save()

    def __str__(self):
        return '%s - %s' % (self.product_related, self.title)

    def check_product_in_order(self):
        return str(self.product_related + '. Χρώμα : ' + self.title.title + ', Μέγεθος : ' + self.title.title)

    def delete_update_product(self):
        self.product_related.qty -= self.qty
        self.product_related.save()

    def tag_final_price(self):
        final_price = self.product_related.final_price if not self.product_related.price_buy == self.price_buy else self.price_buy
        return '%s %s' % (final_price, CURRENCY)

    tag_final_price.short_description = 'Τιμή Αγοράς'

    @staticmethod
    def filters_data(request, queryset):
        size_name = request.GET.getlist('size_name', None)
        queryset = queryset.filter(title__id__in=size_name) if size_name else queryset
        return queryset
