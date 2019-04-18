import django_tables2 as tables
from django.utils.html import format_html
from .models import InvoiceImage
from catalogue.product_details import VendorPaycheck
from .models import Invoice


class ImageColumn(tables.Column):
    def render(self, value):
        return format_html('<img class="img-thumbnail" style="width:100px;height:100px" src="/media/{}" />', value)


class InvoiceImageTable(tables.Table):
    file = ImageColumn()
    edit_button = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>")

    class Meta:
        model = InvoiceImage
        fields = ['id', 'file']
        template_name = 'django_tables2/bootstrap.html'


class PaycheckTable(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>",
                                    orderable=False,
                                    )

    class Meta:
        model = VendorPaycheck
        fields = ['date_expired', 'vendor', 'payment_method', 'value', 'is_paid']
        template_name = 'django_tables2/bootstrap.html'


class InvoiceTable(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>",
                                   orderable=False,
                                   )
    tag_clean_value = tables.Column(orderable=False, verbose_name='Clean Value')
    tag_final_value = tables.Column(orderable=False, verbose_name='Value')

    class Meta:
        model = Invoice
        fields = ['id', 'date_expired', 'title', 'order_type', 'vendor', 'tag_clean_value', 'tag_final_value']
        template_name = 'django_tables2/bootstrap.html'
