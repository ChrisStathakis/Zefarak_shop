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
    for ele in old_object.category_site.all():
        object.category_site.add(ele)
    for ele in old_object.characteristics.all():
        object.characteristics.add(ele)

    for ele in old_object.attr_class.all():
        new_attr_class = AttributeProductClass.objects.create(product_related=object, class_related=ele.class_related)
        for title in ele.my_attributes.all():
            Attribute.objects.create(
                title=title,
                class_related=new_attr_class
            )
    object.save()
    return redirect(object.get_edit_url())
