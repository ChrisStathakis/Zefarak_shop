from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum

from .payroll import Payroll, Employee, Occupation
from .forms import EmployeeForm
from site_settings.models import Store


@method_decorator(staff_member_required, name='dispatch')
class PayrollHomepageView(ListView):
    template_name = 'warehouse/payroll/homepage.html'
    model = Payroll
    paginate_by = 20

    def get_queryset(self):
        queryset = Payroll.browser.get_queryset().not_paid()
        return queryset[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        occupations = Occupation.objects.filter(active=True)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PayrollListView(ListView):
    model = Payroll
    template_name = ''
    paginate_by = 50

    def get_queryset(self):
        queryset = Payroll.objects.all()
        return queryset


@method_decorator(staff_member_required, name='dispatch')
class PayrollCreateView(CreateView):
    pass


@method_decorator(staff_member_required, name='dispatch')
class EmployeeListView(ListView):
    model = Employee
    template_name = 'warehouse/payroll/person_list_view.html'

    def get_queryset(self):
        queryset = Employee.objects.all()
        queryset = Employee.filters_data(self.request, queryset)
        return queryset


@method_decorator(staff_member_required, name='dispatch')
class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:payroll_employee')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New Employee Created')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create New Employee'
        back_url, delete_url = self.success_url, None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class EmployeeEditView(UpdateView):
    pass