from django.utils.html import format_html
import django_tables2 as tables
from catalogue.models import Product
from catalogue.categories import WarehouseCategory


class ImageColumn(tables.Column):

    def render(self, value):
        return format_html('<img class="img img-thumbnail" style="width:50px;height:50px" src="/media/{}" />', value)


class TableProduct(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>", orderable=False)
    tag_final_price = tables.Column(orderable=False, verbose_name='Price')
    tag_price_buy = tables.Column(orderable=False, verbose_name='Price Buy')

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['id', 'title', 'vendor', 'tag_price_buy', 'tag_final_price', 'qty', 'category', 'active', 'action']


class WarehouseCategoryTable(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>",
                                   orderable=False)

    class Meta:
        model = WarehouseCategory
        template_name = 'django_tables2/bootstrap.html'
        fields = ['id', 'title', 'active']
