from django.db import models


class RangeProduct(models.Model):
    range = models.ForeignKey('voucher.Range', on_delete=models.CASCADE)
    product = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE)
    display_order = models.IntegerField(default=0)

    class Meta:
        app_label = 'voucher'


class Range(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    includes_all_products = models.BooleanField(default=False)
    included_products = models.ManyToManyField('catalogue.Product', related_name='includes', blank=True, through=RangeProduct)
    excluded_products = models.ManyToManyField(
        'catalogue.Product', related_name='excludes', blank=True,
        verbose_name=_("Excluded Products"))
    classes = models.ManyToManyField(
        'catalogue.ProductClass', related_name='classes', blank=True,
        verbose_name=_("Product Types"))
    included_categories = models.ManyToManyField(
        'catalogue.Category', related_name='includes', blank=True,
        verbose_name=_("Included Categories"))

    class Meta:
        app_label = 'voucher'


class Benefit(models.Model):
    # Benefit types
    PERCENTAGE, FIXED, MULTIBUY, FIXED_PRICE = (
        "Percentage", "Absolute", "Multibuy", "Fixed price")
    SHIPPING_PERCENTAGE, SHIPPING_ABSOLUTE, SHIPPING_FIXED_PRICE = (
        'Shipping percentage', 'Shipping absolute', 'Shipping fixed price')
    TYPE_CHOICES = (
        (PERCENTAGE, _("Discount is a percentage off of the product's value")),
        (FIXED, _("Discount is a fixed amount off of the product's value")),
        (MULTIBUY, _("Discount is to give the cheapest product for free")),
        (FIXED_PRICE,
         _("Get the products that meet the condition for a fixed price")),
        (SHIPPING_ABSOLUTE,
         _("Discount is a fixed amount of the shipping cost")),
        (SHIPPING_FIXED_PRICE, _("Get shipping for a fixed price")),
        (SHIPPING_PERCENTAGE, _("Discount is a percentage off of the shipping"
                                " cost")),
    )
    type = models.CharField(
        _("Type"), max_length=128, choices=TYPE_CHOICES, blank=True)

    # The value to use with the designated type.  This can be either an integer
    # (eg for multibuy) or a decimal (eg an amount) which is slightly
    # confusing.
    value = models.DecimalField(
        _("Value"), decimal_places=2, max_digits=12, null=True, blank=True)

    # If this is not set, then there is no upper limit on how many products
    # can be discounted by this benefit.
    max_affected_items = models.PositiveIntegerField(
        _("Max Affected Items"), blank=True, null=True,
        help_text=_("Set this to prevent the discount consuming all items "
                    "within the range that are in the basket."))


class Condition(models.Model):
    """
      A condition for an offer to be applied. You can either specify a custom
      proxy class, or need to specify a type, range and value.
      """
    COUNT, VALUE, COVERAGE = ("Count", "Value", "Coverage")
    TYPE_CHOICES = (
        (COUNT, _("Depends on number of items in basket that are in "
                  "condition range")),
        (VALUE, _("Depends on value of items in basket that are in "
                  "condition range")),
        (COVERAGE, _("Needs to contain a set number of DISTINCT items "
                     "from the condition range")))
    range = models.ForeignKey(
        'offer.Range',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Range"))
    type = models.CharField(_('Type'), max_length=128, choices=TYPE_CHOICES,
                            blank=True)
    value = fields.PositiveDecimalField(
        _('Value'), decimal_places=2, max_digits=12, null=True, blank=True)

    proxy_class = fields.NullCharField(
        _("Custom class"), max_length=255, default=None)

    class Meta:
        abstract = True
        app_label = 'offer'


class ConditionalOffer(models.Model):
    name = models.CharField(unique=True, max_length=150, help_text=_("This is displayed within the customer's basket"))
    description = models.TextField()

    SITE, VOUCHER, USER, SESSION = ("Site", "Voucher", "User", "Session")
    TYPE_CHOICES = (
        (SITE, _("Site offer - available to all users")),
        (VOUCHER, _("Voucher offer - only available after entering "
                    "the appropriate voucher code")),
        (USER, _("User offer - available to certain types of user")),
        (SESSION, _("Session offer - temporary offer, available for "
                    "a user for the duration of their session")),
    )
    offer_type = models.CharField(
        _("Type"), choices=TYPE_CHOICES, default=SITE, max_length=128)

    exclusive = models.BooleanField(
        _("Exclusive offer"),
        help_text=_("Exclusive offers cannot be combined on the same items"),
        default=True
    )

    OPEN, SUSPENDED, CONSUMED = "Open", "Suspended", "Consumed"
    status = models.CharField(_("Status"), max_length=64, default=OPEN)

    condition = models.ForeignKey(
        Condition,
        on_delete=models.CASCADE,
        related_name='offers',
        verbose_name=_("Condition"))
    benefit = models.ForeignKey(
        Benefit,
        on_delete=models.CASCADE,
        related_name='offers',
        verbose_name=_("Benefit"))

    # Some complicated situations require offers to be applied in a set order.
    priority = models.IntegerField(
        _("Priority"), default=0, db_index=True,
        help_text=_("The highest priority offers are applied first"))

    # AVAILABILITY

    # Range of availability.  Note that if this is a voucher offer, then these
    # dates are ignored and only the dates from the voucher are used to
    # determine availability.
    start_datetime = models.DateTimeField(
        _("Start date"), blank=True, null=True,
        help_text=_("Offers are active from the start date. "
                    "Leave this empty if the offer has no start date."))
    end_datetime = models.DateTimeField(
        _("End date"), blank=True, null=True,
        help_text=_("Offers are active until the end date. "
                    "Leave this empty if the offer has no expiry date."))

    # Use this field to limit the number of times this offer can be applied in
    # total.  Note that a single order can apply an offer multiple times so
    # this is not necessarily the same as the number of orders that can use it.
    # Also see max_basket_applications.
    max_global_applications = models.PositiveIntegerField(
        _("Max global applications"),
        help_text=_("The number of times this offer can be used before it "
                    "is unavailable"), blank=True, null=True)

    # Use this field to limit the number of times this offer can be used by a
    # single user.  This only works for signed-in users - it doesn't really
    # make sense for sites that allow anonymous checkout.
    max_user_applications = models.PositiveIntegerField(
        _("Max user applications"),
        help_text=_("The number of times a single user can use this offer"),
        blank=True, null=True)

    # Use this field to limit the number of times this offer can be applied to
    # a basket (and hence a single order). Often, an offer should only be
    # usable once per basket/order, so this field will commonly be set to 1.
    max_basket_applications = models.PositiveIntegerField(
        _("Max basket applications"),
        blank=True, null=True,
        help_text=_("The number of times this offer can be applied to a "
                    "basket (and order)"))

    # Use this field to limit the amount of discount an offer can lead to.
    # This can be helpful with budgeting.
    max_discount = models.DecimalField(
        _("Max discount"), decimal_places=2, max_digits=12, null=True,
        blank=True,
        help_text=_("When an offer has given more discount to orders "
                    "than this threshold, then the offer becomes "
                    "unavailable"))

    # TRACKING
    # These fields are used to enforce the limits set by the
    # max_* fields above.

    total_discount = models.DecimalField(
        _("Total Discount"), decimal_places=2, max_digits=12,
        default=D('0.00'))
    num_applications = models.PositiveIntegerField(
        _("Number of applications"), default=0)
    num_orders = models.PositiveIntegerField(
        _("Number of Orders"), default=0)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    objects = models.Manager()


    # We need to track the voucher that this offer came from (if it is a
    # voucher offer)
    _voucher = None
