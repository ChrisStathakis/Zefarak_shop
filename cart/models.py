from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from .managers import CartManager
from .validators import validate_positive_decimal
from site_settings.models import Shipping, PaymentMethod
from site_settings.constants import CURRENCY
from catalogue.models import Product
from catalogue.product_attritubes import Attribute


User = get_user_model()


class Cart(models.Model):
    cart_id = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, blank=True, related_name='carts', on_delete=models.CASCADE)
    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (MERGED, _("Merged - superceded by another basket")),
        (SAVED, _("Saved - for items to be purchased later")),
        (FROZEN, _("Frozen - the basket cannot be modified")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )
    status = models.CharField(
        _("Status"), max_length=128, default=OPEN, choices=STATUS_CHOICES)

    vouchers = ''
    timestamp = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    date_merged = models.DateTimeField(_("Date merged"), null=True, blank=True)
    date_submitted = models.DateTimeField(_("Date submitted"), null=True,
                                          blank=True)
    editable_statuses = (OPEN, SAVED)

    my_query = CartManager()
    objects = models.Manager()

    shipping_method = models.ForeignKey(Shipping, blank=True, null=True, on_delete=models.SET_NULL)
    payment_method = models.ForeignKey(PaymentMethod, blank=True, null=True, on_delete=models.SET_NULL)
    # coupon = models.ManyToManyField(Coupons)
    # coupon_discount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    final_value = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    value = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, validators=[validate_positive_decimal, ])
    discount_value = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return f'Cart {self.id}'

    def save(self, *args, **kwargs):
        cart_items = self.cart_items.all()
        self.value = cart_items.aggregate(Sum('total_value'))['total_value__sum'] if cart_items else 0
        self.final_value = self.value - self.discount_value
        super().save(*args, **kwargs)

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'

    def tag_value(self):
        return f'{self.value} {CURRENCY}'

    def tag_discount_value(self):
        return f'{self.discount_value} {CURRENCY}'

    def get_edit_url(self):
        return reverse('cart:cart_detail', kwargs={'pk': self.id})

    @staticmethod
    def filter_data(request, queryset=None):
        queryset = queryset if queryset else Cart.objects.all()
        search_name = request.GET.get('search_name', None)
        status_name = request.GET.getlist('status_name', None)
        queryset = queryset.filter(status__in=status_name) if status_name else queryset
        queryset = queryset.filter(user__username__contains=search_name) if search_name else queryset
        return queryset


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    have_attributes = models.BooleanField(default=False)
    value = models.DecimalField(default=0, decimal_places=2, max_digits=10,
                                validators=[validate_positive_decimal,
                                            ])
    price_discount = models.DecimalField(default=0, decimal_places=2, max_digits=10,
                                         validators=[validate_positive_decimal, ]
                                         )
    final_value = models.DecimalField(default=0, decimal_places=2, max_digits=10,
                                      validators=[validate_positive_decimal, ])
    total_value = models.DecimalField(default=0, decimal_places=2, max_digits=10,
                                      validators=[validate_positive_decimal, ])
    objects = models.Manager()

    def __str__(self):
        return f'{self.cart} - {self.product}'

    def save(self, *args, **kwargs):
        self.final_value = self.price_discount if self.price_discount > 0 else self.value
        self.total_value = self.get_total_value()
        super().save(*args, **kwargs)
        self.cart.save()

    def get_remove_url(self):
        return reverse('cart:check', kwargs={'pk': self.id, 'action': 'remove'})

    def get_ajax_change_qty_url(self):
        return reverse('cart:ajax_change_qty', kwargs={'pk': self.id})

    def get_total_value(self):
        return self.qty * self.final_value

    def tag_value(self):
        return '%s %s' % (round(self.value, 2), CURRENCY)

    def tag_total_value(self):
        return f'{self.total_value} {CURRENCY}'

    def tag_final_value(self):
        return '%s %s' % (self.final_value, CURRENCY)

    @staticmethod
    def create_cart_item(request, cart, product, qty, attributes=[]):
        product_qty = product.qty
        if qty > product_qty:
            return ''
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.value = product.price
        cart_item.price_discount = product.price_discount

        if product.product_class.is_service or not product.product_class.have_transcations:
            cart_item.save()
            return cart_item

        cart_item.have_attributes = True
        cart_item.qty = qty if created else cart_item.qty + qty
        if not product.product_class.have_attribute:
            cart_item.save()
            return cart_item

        for attr in attributes:
            new_attr = CartAttribute.objects.get_or_create(cart_item=cart_item, attribute=attr)
        cart_item.save()
        return cart_item


@receiver(post_delete, sender=CartItem)
def update_order_on_delete(sender, instance, *args, **kwargs):
    cart = instance.cart
    for ele in instance.cart_attributes.all():
        ele.delete()
    cart.save()


class CartAttribute(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='cart_attributes')
    attribute = models.ForeignKey(Attribute, null=True, on_delete=models.SET_NULL)




'''
class CartRules(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    coupons = models.ManyToManyField(Coupons)
    payment_value = models.PositiveIntegerField(default=0)
    shipping_value = models.PositiveIntegerField(default=0)

    def estimate_shipping_value(self):
        value = self.cart.value
        shipping_method = self.cart.shipping_method
        shipping_value = 5
        if shipping_method:
            shipping_value = shipping_method.value if shipping_method.value_limit < value else 0
        return shipping_value

    def estimate_payment_type(self):
        payment_method = self.cart.payment_method
        payment_value = 2
        if payment_method:
            payment_value = 5 if payment_method == 1 and payment_method else 0
        return payment_value

    def save(self, *args, **kwargs):
        self.payment_value = self.estimate_payment_type()
        self.shipping_value = self.estimate_shipping_value()
        super(CartRules, self).save(*args, **kwargs)


class CartGiftItem(models.Model):
    cart_related = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='gifts')
    product_related = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.cart_related

    @staticmethod
    def check_cart(cart):
        if cart:
            gifts = cart.gifts.all()
            gifts.delete()
            items = cart.cart_items.all()
            for item in items:
                can_be_gift = Gifts.objects.filter(product_related=item.product_related)
                if can_be_gift.exists:
                    for gift in can_be_gift:
                        new_gift = CartGiftItem.objects.create(product_related=gift.products_gift,
                                                               cart_related=cart,
                                                               qty=item.qty
                                                               )

'''