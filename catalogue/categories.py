from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from mptt.models import MPTTModel, TreeForeignKey

from .managers import CategoryManager
from .validators import category_site_directory_path
from site_settings.constants import MEDIA_URL, CURRENCY


class WarehouseCategory(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(unique=True, max_length=70, verbose_name='Τίτλος Κατηγορίας')
    description = models.TextField(null=True, blank=True, verbose_name='Περιγραφή')

    class Meta:
        app_label = 'catalogue'
        ordering = ['title']
        verbose_name = "3. Κατηγορίες Αποθήκης"
        verbose_name_plural = '3. Κατηγορίες Αποθήκης'

    def __str__(self):
        return self.title


class Category(MPTTModel):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=120)
    image = models.ImageField(blank=True, null=True, upload_to=category_site_directory_path, help_text='610*410')
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateField(auto_now=True)
    meta_description = models.CharField(max_length=300, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=1)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    show_on_menu = models.BooleanField(default=False, verbose_name='Active on Navbar')
    browse = CategoryManager()
    objects = models.Manager()

    class Meta:
        app_label = 'catalogue'
        verbose_name_plural = '3. Κατηγορίες Site'
        unique_together = ('slug', 'parent' )
        ordering = ['-order', ]

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def image_tag(self):
        if self.image:
            return mark_safe('<img scr="%s%s" width="400px" height="400px" />' % (MEDIA_URL, self.image))

    def image_tag_tiny(self):
        if self.image:
            return mark_safe('<img scr="%s%s" width="100px" height="100px" />' % (MEDIA_URL, self.image))

    image_tag.short_description = 'Είκονα'

    def tag_active(self):
        return 'Is Active' if self.active else 'No active'

    def tag_show_on_menu(self):
        return 'Show' if self.show_on_menu else 'No Show'

    def get_edit_url(self):
        return reverse('dashboard:category_edit_view', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('category_page', kwargs={'slug': self.slug})

    def absolute_url_site(self):
        pass

    def get_childrens(self):
        childrens = self.children.all()
        return childrens

    @staticmethod
    def filter_data(queryset, request):
        search_name = request.GET.get('search_name', None)
        active_name = request.GET.getlist('active_name', None)
        menu_name = request.GET.getlist('menu_name', None)
        print(menu_name)
        queryset = queryset.filter(name__icontains=search_name) if search_name else queryset
        queryset = queryset.filter(active=True) if active_name else queryset
        queryset = queryset.filter(show_on_menu=True) if 'a' in menu_name else queryset.filter(show_on_menu=False) if 'b' in menu_name else queryset
        return queryset
