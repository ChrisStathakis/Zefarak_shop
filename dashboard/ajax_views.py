from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from catalogue.categories import Category
from catalogue.models import Product, ProductPhotos
from catalogue.product_attritubes import AttributeTitle, AttributeProductClass, Attribute

from catalogue.forms import CategorySiteForm, BrandForm
from decimal import Decimal


@staff_member_required
def ajax_category_site(request, slug,  pk, dk):
    instance = get_object_or_404(Product, id=pk)
    category = get_object_or_404(Category, id=dk)
    if slug == 'add':
        instance.category_site.add(category)
    if slug == 'delete':
        instance.category_site.remove(category)
    instance.save()
    selected_data = instance.category_site.all()
    data = dict()
    data['result'] = render_to_string(template_name='dashboard/catalogue/ajax_calls/result_container.html',
                                      request=request,
                                      context={'selected_data': selected_data,
                                               'instance': instance
                                               }
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_product_images(request, slug, pk, dk):
    instance = get_object_or_404(Product, id=pk)
    image = get_object_or_404(ProductPhotos, id=dk)
    if slug == 'is_primary':
        queryset = instance.images.all()
        queryset.update(is_primary=False)
        image.is_primary = True
        image.save()
    if slug == 'delete':
        image.delete()
    data = dict()
    instance.refresh_from_db()
    photos = instance.images.all()
    data['result'] = render_to_string(template_name='dashboard/catalogue/ajax_calls/images.html',
                                      request=request,
                                      context={'photos': photos,
                                               'instance': instance
                                               }
                                      )
    return JsonResponse(data)


def ajax_add_or_delete_attribute(request, slug, pk, dk):
    instance = get_object_or_404(AttributeProductClass, id=pk)
    attr_class = instance
    attr_title = get_object_or_404(AttributeTitle, id=dk)
    if slug == 'add':
        my_attr, created = Attribute.objects.get_or_create(product_related=instance.product_related,
                                                           class_related=instance,
                                                           title=attr_title
                                                           )
    if slug == 'delete':
        my_attr, created = Attribute.objects.get_or_create(product_related=instance.product_related,
                                                           class_related=instance,
                                                           title=attr_title
                                                           )
        my_attr.delete()
    data = dict()
    attr_class.refresh_from_db()
    selected_data = instance.my_attributes.all()
    data['result'] = render_to_string(template_name='dashboard/catalogue/ajax_calls/result_container_attr.html',
                                      request=request,
                                      context={
                                          'selected_data': selected_data,
                                          'attr_class': attr_class
                                      })
    return JsonResponse(data)


@staff_member_required
def ajax_add_or_delete_related_item(request, pk, dk):
    data = {}
    instance = get_object_or_404(Product, id=pk)
    related_instance = get_object_or_404(Product, id=dk)
    instance.related_products.add(related_instance)
    related_products = instance.related_products.all()
    data['html_data'] = render_to_string(request=request, template_name='dashboard/ajax_calls/related.html',
                                         context=locals())
    return JsonResponse(data)


@staff_member_required
def ajax_change_qty_on_attribute(request, pk):
    attr_data = get_object_or_404(Attribute, id=pk)
    qty = request.GET.get('qty', 1)
    try:
        qty = float(qty)
    except:
        qty = qty
    if isinstance(qty, (int, float, )):
        attr_data.qty = qty
        attr_data.save()
    selected_data = attr_data.product_related.attributes.all()
    attr_class = attr_data.class_related
    data = dict()
    return JsonResponse(data)


def popup_category(request):
    form = CategorySiteForm(request.POST or None)
    form_title = 'Create category'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))
    return render(request, "dashboard/settings/form.html", {"form": form, 'form_title': form_title})


def popup_brand(request):
    form = BrandForm(request.POST or None)
    form_title = 'Create Brand'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_brand");</script>' % (instance.pk, instance))
    return render(request, "dashboard/settings/form.html", locals())
