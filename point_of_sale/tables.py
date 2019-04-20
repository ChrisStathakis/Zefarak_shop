from django.utils.html import format_html
import django_tables2 as tables

from accounts.models import Profile
from .models import Order, OrderItem


class ProfileTable(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>", orderable=False)

    class Meta:
        model = Profile
        template_name = 'django_tables2/bootstrap.html'
        fields = ['first_name', 'last_name', 'cellphone', 'tag_balance']


class OrderTable(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>", orderable=False)
    tag_final_value = tables.Column(orderable=False, verbose_name='Value')

    class Meta:
        model = Order
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date_expired', 'title', 'order_type', 'profile', 'status','tag_final_value']
