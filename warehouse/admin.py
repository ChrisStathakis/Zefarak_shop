from django.contrib import admin
from .billing import BillInvoice, BillCategory
from .payroll import Payroll, Employee, Occupation
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(BillCategory)
class BillCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title', 'store__title']
    list_display = ['__str__', 'tag_balance', 'active']
    list_filter = ['active', 'store']
    readonly_fields = ['tag_balance']
    fields = ['active', 'store', 'title', 'tag_balance']
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        my_read_only_fields = self.readonly_fields
        if obj:
            my_read_only_fields.append('store')
        return my_read_only_fields


@admin.register(BillInvoice)
class BillInvoiceAdmin(admin.ModelAdmin):
    search_fields = ['title', 'category__title', 'category__store__title']
    save_as = True
    autocomplete_fields = ['category', ]
    list_display = ['date_expired', 'title', 'category', 'payment_method', 'tag_final_value', 'is_paid']
    list_filter = ['category', 'is_paid', 'date_expired']
    list_select_related = ['payment_method', 'category']
    readonly_fields = ['tag_final_value']
    fieldsets = (
        ('General Data', {
            'fields': (('date_expired', 'category'),
                       ('title', 'notes'),
                       )
        }),
        ('Price', {
            'fields': (('value', 'payment_method', 'is_paid'), )
        }),


    )

    def save_model(self, request, obj, form, change):
        if '_saveasnew' in request.POST:
            obj.is_paid = False
            return super().save_model(request, obj, form, change)
        return super().save_model(request, obj, form, change)


@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ['title',  'active']
    list_filter = ['active', ]
    fields = ['active', 'title', 'notes']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone', 'tag_balance', 'active']
    list_select_related = ['occupation']
    list_filter = ['occupation', 'active']
    readonly_fields = ['tag_balance', 'timestamp', 'edited']
    fieldsets = (
        ('General Info', {
            'fields': ('active', 'tag_balance',
                       ('title', 'date_added'),
                       ('timestamp', 'edited')
                       )
        }),
        ('Edit', {
            'fields': (('occupation', 'store'),
                       ('phone', 'phone1'),
                       ('vacation_days',)
                       )
        }),
    )


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_expired'
    list_per_page = 50
    list_select_related = ['payment_method', 'employee', 'user_account', 'person']
    list_display = ['date_expired', 'employee', 'category', 'tag_final_value', 'payment_method', 'is_paid']
    list_filter = ['is_paid', 'date_expired', 'category', 'user_account', 'payment_method']
    fieldsets = (
        ('General', {
            'fields': (
                'is_paid',
                ('title', 'date_expired', 'person'),
                ('timestamp', 'edited'),
                ('tag_final_value', 'user_account'),
                )
        }),
        ('Edit Data', {
            'fields': (
                ('value', 'payment_method', 'category'),
                ('tag_paid_value')
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.user_account:
            obj.user_account = request.user
        super(PayrollAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        my_list = ['timestamp', 'edited', 'user_account', 'tag_paid_value', 'tag_final_value']
        if obj:
            my_list.append('person')
            if obj.is_paid:
                my_list.append('value')
        return my_list
