from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from catalogue.models import Product


@staff_member_required
def copy_product_view(request, pk):
    old_object = get_object_or_404(Product, id=pk)
    object = get_object_or_404(Product, id=pk)
    object.id = None
    object.qty = 0
    object.slug = None
    object.save()
    for ele in old_object.category_site.all():
        object.category_site.add(ele)
    for ele in old_object.characteristics.all():
        object.characteristics.add(ele)
    object.save()
    return redirect(object.get_edit_url())
