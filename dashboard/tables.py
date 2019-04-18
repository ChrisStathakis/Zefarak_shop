from django.utils.html import format_html
import django_tables2 as tables
from catalogue.models import Product


class ImageColumn(tables.Column):

    def render(self, value):
        return format_html('<img class="img-thumbnail" style="width:100px;height:100px" src="/media/{}" />', value)


class TableProduct(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>", orderable=False)
    image = ImageColumn()
    tag_final_value = tables.Column(orderable=False, verbose_name='Value')

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['image', 'id', 'title', 'vendor', 'category', 'tag_final_value', 'qty', 'active', 'action']