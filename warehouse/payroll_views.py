from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum

from .payroll import Payroll, Employee, Occupation, PAYROLL_CHOICES
from .forms import EmployeeForm, OccupationForm, PayrollForm
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
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class EmployeeListCardView(ListView):
    model = Employee
    template_name = 'warehouse/payroll/employee_card_list.html'

    def get_queryset(self):
        queryset = Employee.objects.filter(active=True)
        return queryset


@method_decorator(staff_member_required, name='dispatch')
class EmployeeCardView(ListView):
    model = Payroll
    template_name = 'warehouse/payroll/employee_card_detail.html'
    paginate_by = 20

    def get_queryset(self):
        self.employee = get_object_or_404(Employee, id=self.kwargs['pk'])
        queryset = Payroll.objects.filter(employee=self.employee)
        queryset = Payroll.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.employee
        categories = PAYROLL_CHOICES
        back_url = reverse('warehouse:employee-card-list')
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
    model = Payroll
    form_class = PayrollForm
    template_name = 'warehouse/form.html'

    def get_initial(self):
        initial = super().get_initial()
        self.employee = get_object_or_404(Employee, id=self.kwargs['pk'])
        initial['employee'] = self.employee
        return initial

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Create Payroll for {self.employee}'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New payroll Added')
        return self.form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class PayrollUpdateView(UpdateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'warehouse/form.html'

    def get_success_url(self):
        return reverse('warehouse:employee-card-detail', kwargs={'pk': self.object.employee.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit Payroll {self.object.title}'
        back_url, delete_url = self.get_success_url(), reverse('warehouse:payroll_delete', kwargs={'pk': self.object.id})
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Payroll is Edit')
        return super().form_valid(form)


@staff_member_required
def delete_payroll(request, pk):
    instance = get_object_or_404(Payroll, id=pk)
    instance.delete()
    messages.success(request, 'The Payroll is deleted')
    return redirect(reverse('warehouse:employee-card-detail', kwargs={'pk': instance.employee.id}))


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
    model = Employee
    form_class = EmployeeForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:payroll_employee')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'{self.object.title} Edited Corectly')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for_title = f'Edit {self.object.title}'
        back_url, delete_url = self.success_url, ''
        context.update(locals())
        return context


@staff_member_required
def delete_employee(request, pk):
    instance = get_object_or_404(Employee, id=pk)
    if instance.person_invoices.exists():
        messages.warning(request, 'You cant delete this employee')
    else:
        instance.delete()
    return redirect(reverse('warehouse:payroll_employee'))


@method_decorator(staff_member_required, name='dispatch')
class OccupationListView(ListView):
    model = Occupation
    template_name = 'warehouse/payroll/occup_list_view.html'

    def get_queryset(self):
        queryset = Occupation.objects.all()
        queryset = Occupation.filters_data(self.request, queryset)
        return queryset


@method_decorator(staff_member_required, name='dispatch')
class OccupationCreateView(CreateView):
    model = Occupation
    form_class = OccupationForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:occupation_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New Occupation is saved')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create New Occupation'
        back_url, delete_url = self.success_url, None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class OccupationUpdateView(UpdateView):
    model = Occupation
    form_class = OccupationForm
    template_name = 'warehouse/form.html'
    success_url = reverse_lazy('warehouse:occupation_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The Occupation is saved')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object.title}'
        back_url, delete_url = self.success_url, reverse('warehouse:occupation_delete', kwargs={'pk': self.object.id})
        context.update(locals())
        return context


@staff_member_required
def delete_occupation(request, pk):
    instance = get_object_or_404(Occupation, id=pk)
    instance.delete()
    return redirect(reverse('warehouse:occupation_list'))


@staff_member_required
def payroll_quick_pay(request, pk):
    instance = get_object_or_404(Payroll, id=pk)
    instance.is_paid = True
    instance.save()
    messages.success(request, 'The payroll is Paid')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


