from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.forms import formset_factory, inlineformset_factory
from django.conf import settings
from django.db import connection
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

from catalogue.models import Product, ProductPhotos, ProductClass
from catalogue.categories import Category
from catalogue.product_details import Brand, Vendor
from catalogue.forms import (CreateProductClassForm, CategorySiteForm,
                             BrandForm, CharacteristicsValueForm,
                             CharacteristicsForm, AttributeClassForm, AttributeTitleForm
                             )
from catalogue.product_attritubes import (ProductCharacteristics, Characteristics, CharacteristicsValue,
                                          Attribute, AttributeTitle, AttributeClass
                                          )

CURRENCY = settings.CURRENCY


@method_decorator(staff_member_required, name='dispatch')
class ProductClassView(ListView):
    model = ProductClass
    template_name = 'dashboard/settings/product_class_list.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(locals())
        return context


class ProductClassCreateView(CreateView):
    model = ProductClass
    form_class = CreateProductClassForm
    template_name = 'dashboard/settings/form.html'
    success_url = reverse_lazy('dashboard:product_class_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create Product Class'
        back_url, delete_url = reverse('dashboard:product_class_view'), None
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New Product class Added')
        return super(ProductClassCreateView, self).form_valid(form)


# -- CATEGORY SITE

@method_decorator(staff_member_required, name='dispatch')
class CategorySiteListView(ListView):
    template_name = 'dashboard/settings/category_site_list.html'
    model = Category
    paginate_by = 50

    def get_queryset(self):
        queryset = Category.objects.all()
        queryset = Category.filter_data(queryset, self.request)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategorySiteListView, self).get_context_data(**kwargs)
        page_title = 'Site Categories'
        context.update(locals())
        context.update(self.request.GET)
        return context


@method_decorator(staff_member_required, name='dispatch')
class CategorySiteEditView(UpdateView):
    model = Category
    form_class = CategorySiteForm
    template_name = 'dashboard/settings/form.html'
    success_url = reverse_lazy('dashboard:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = reverse('dashboard:category_list'),\
                               reverse('dashboard:delete_category_site', kwargs={'pk': self.kwargs.get('pk')})
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The category edited successfuly!')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class CategorySiteCreateView(CreateView):
    model = Category
    template_name = 'dashboard/settings/form.html'
    form_class = CategorySiteForm
    success_url = reverse_lazy('dashboard:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create New Site Category'
        back_url, delete_url = reverse('dashboard:category_list'), None
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New category added!')
        return super().form_valid(form)


@staff_member_required
def delete_category_site(request, pk):
    instance = get_object_or_404(Category, id=pk)
    instance.delete()
    messages.warning(request, f'The category {instance.name} is deleted')
    return HttpResponseRedirect(reverse('dashboard:category_list'))


#  -- BRANDS


@method_decorator(staff_member_required, name='dispatch')
class BrandListView(ListView):
    template_name = 'dashboard/settings/brand_list.html'
    model = Brand
    paginate_by = 50

    def get_queryset(self):
        queryset = Brand.objects.all()
        queryset = Brand.filters_data(queryset, self.request)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(locals())
        context.update(self.request.GET)
        return context


@method_decorator(staff_member_required, name='dispatch')
class BrandEditView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'dashboard/settings/form.html'
    success_url = reverse_lazy('dashboard:brand_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object.title}'
        back_url, delete_url = self.success_url, reverse('dashboard:delete_brand', kwargs={'pk': self.object.id})
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The brand is updated!')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'dashboard/settings/form.html'
    success_url = reverse_lazy('dashboard:brand_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create Brand'
        back_url, delete_url = reverse('dashboard:brand_list_view'), None
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The Brand Created!')
        return super().form_valid(form)


@staff_member_required
def delete_brand(request, pk):
    instance = get_object_or_404(Brand, id=pk)
    instance.delete()
    messages.warning(request, 'The brand %s has deleted' % instance.title)
    return redirect(reverse('dashboard:brand_list_view'))


@method_decorator(staff_member_required, name='dispatch')
class CharacteristicsListView(ListView):
    model = Characteristics
    template_name = 'dashboard/settings/characteristics_list.html'
    paginate_by = 50


@staff_member_required
def characteristics_detail_view(request, pk):
    instance = get_object_or_404(Characteristics, id=pk)
    form = CharacteristicsForm(instance=instance)
    add_form = CharacteristicsValueForm(initial={'char_related': instance})
    if request.POST:
        if 'add_form' in request.POST:
            add_form = CharacteristicsValueForm(request.POST, initial={'char_related': instance})
            if add_form.is_valid():
                add_form.save()
                messages.success(request, 'The Value added')
                return HttpResponseRedirect(instance.get_edit_url())
    if request.POST:
        if 'edit_form' in request.POST:
            form = CharacteristicsForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'The Char is Edited!')
                return HttpResponseRedirect(instance.get_edit_url())
    context = locals()
    return render(request, 'dashboard/settings/characteristic_detail_view.html', context)


@method_decorator(staff_member_required, name='dispatch')
class CharacterCreateView(CreateView):
    model = Characteristics
    template_name = 'dashboard/settings/form.html'
    form_class = CharacteristicsForm
    success_url = reverse_lazy('dashboard:characteristics_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        back_url, delete_url = self.success_url, None
        form_title = 'Create New Characteristic'
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New Characteristic added')
        return super().form_valid(form)


@staff_member_required
def characteristic_delete_view(request, pk):
    instance = get_object_or_404(Characteristics, id=pk)
    for ele in instance.char_details.all():
        ele.delete()
    instance.delete()
    messages.warning(request, 'The Characteristic is deleted!')
    return redirect(reverse('dashboard:characteristics_list_view'))


@method_decorator(staff_member_required, name='dispatch')
class CharValueEditView(UpdateView):
    model = CharacteristicsValue
    form_class = CharacteristicsValueForm
    template_name = 'dashboard/settings/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        back_url, delete_url = self.get_success_url(), reverse('dashboard:char_value_delete_view', kwargs={'pk': self.object.id})
        form_title = f'Edit {self.object.title}'
        context.update(locals())
        return context

    def get_success_url(self):
        return reverse('dashboard:char_edit_view', kwargs={'pk': self.object.char_related.id})

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The value is edited!')
        return super().form_valid(form)


@staff_member_required
def delete_char_value_view(request, pk):
    instance = get_object_or_404(CharacteristicsValue, id=pk)
    instance.delete()
    messages.success(request, 'The Value is deleted')
    return redirect(reverse('dashboard:char_edit_view', kwargs={'pk': instance.char_related.id}))


@method_decorator(staff_member_required, name='dispatch')
class AttributeClassListView(ListView):
    model = AttributeClass
    template_name = 'dashboard/settings/attribute_class.html'


@method_decorator(staff_member_required, name='dispatch')
class AttributeClassCreateView(CreateView):
    model = AttributeClass
    template_name = 'dashboard/settings/form.html'
    success_url = reverse_lazy('dashboard:attribute_class_list_view')
    form_class = AttributeClassForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Attribute Class Added')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create Attribute Class'
        back_url, delete_url = self.success_url, None
        context.update(locals())
        return context


@staff_member_required
def attribute_class_edit_view(request, pk):
    instance = get_object_or_404(AttributeClass, id=pk)
    add_form = AttributeTitleForm(initial={'attri_by': instance})
    form = AttributeClassForm(instance=instance)
    if request.POST:
        if 'add_form' in request.POST:
            add_form = AttributeTitleForm(request.POST, initial={'attri_by': instance})
            if add_form.is_valid():
                add_form.save()
                messages.success(request, 'New Value added')
                return redirect(reverse('dashboard:attribute_class_edit_view', kwargs={'pk': instance.id}))
        if 'edit_form' in request.POST:
            form = AttributeClassForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'The Attribute is edited')
                return redirect(reverse('dashboard:attribute_class_edit_view', kwargs={'pk': instance.id}))
    context = locals()
    return render(request, 'dashboard/settings/characteristic_detail_view.html', context)


@method_decorator(staff_member_required, name='dispatch')
class AttributeTitleEditView(UpdateView):
    model = AttributeTitle
    form_class = AttributeTitleForm
    template_name = 'dashboard/settings/form.html'

    def get_success_url(self):
        return reverse('dashboard:attribute_class_edit_view', kwargs={'pk': self.object.attri_by.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        back_url, delete_url = self.get_success_url(), ''
        form_title = f'Edit {self.object.title}'

        context.update(locals())
        return context


@staff_member_required
def attribute_class_delete_view(request, pk):
    instance = get_object_or_404(AttributeClass, id=pk)
    for ele in instance.my_values.all():
        ele.delete()
    instance.delete()
    messages.success(request, 'The item i deleted')
    return redirect(reverse('dashboard:attribute_class_list_view'))


@staff_member_required
def attribute_title_delete_view(request, pk):
    instance = get_object_or_404(AttributeTitle, id=pk)
    instance.delete()
    messages.warning(request, 'The item is deleted')
    return redirect(reverse('dashboard:attribute_class_edit_view', kwargs={'pk': instance.attri_by.id}))





