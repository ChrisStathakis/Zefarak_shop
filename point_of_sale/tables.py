from django.utils.html import format_html
import django_tables2 as tables

from accounts.models import Profile, User


class ProfileTable(tables.Table):
    action = tables.TemplateColumn("<a href='{{ record.get_edit_url }}' class='btn btn-primary'>Edit</a>")

    class Meta:
        model = Profile
        template_name = 'django_tables2/bootstrap.html'
        fields = ['first_name', 'last_name', 'cellphone', 'tag_balance']