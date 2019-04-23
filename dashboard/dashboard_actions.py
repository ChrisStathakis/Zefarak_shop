from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from catalogue.models import Product
from catalogue.product_attritubes import Attribute, AttributeProductClass


@staff_member_required
def copy_product_view(request, pk):
    old_object = get_object_or_404(Product, id=pk)
    object = get_object_or_404(Product, id=pk)
    object.id = None
    object.qty = 0
    object.slug = None
    object.save()
    object.refresh_from_db()
    print('new_object', object.id, 'old_object', old_object.id)
    for ele in old_object.category_site.all():
        object.category_site.add(ele)
    for ele in old_object.characteristics.all():
        object.characteristics.add(ele)
    
    for attr_class in old_object.attr_class.all():
        all_attributes = attr_class.my_attributes.all()
        attr_class.id= None
        attr_class.product_related = object
        attr_class.save()
        attr_class.refresh_from_db()
        for title in all_attributes:
            title.id=None
            title.class_related = attr_class
            title.qty = 0
            title.save()
    return redirect(object.get_edit_url())
