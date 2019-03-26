from django.urls import path
from .views import (
    WarehouseDashboard, BillingHomepageView, BillingStoreListView,
    CreateBillingInvoiceView, BillInvoiceEditView, quick_billing_pay,
    delete_bill_invoice_view, CreateBillingCategoryView, EditBillingCategoryView, delete_bill_category_view
    )
from .payroll_views import PayrollHomepageView, EmployeeListView, EmployeeCreateView


app_name = 'warehouse'

urlpatterns = [
    path('', WarehouseDashboard.as_view(), name='dashboard'),
    path('billing-view', BillingHomepageView.as_view(), name='billing_view'),
    path('billing-store-view/<int:pk>/', BillingStoreListView.as_view(), name='billing_store_view'),
    path('billing-create-view/<int:pk>/', CreateBillingInvoiceView.as_view(), name='billing_invoice_create_view'),
    path('billing-invoice-edit-view/<int:pk>/', BillInvoiceEditView.as_view(), name='bill_invoice_edit_view'),
    path('billing-invoice-edit-view-pay/<int:pk>/', quick_billing_pay, name='quick_pay_invoice'),
    path('billing-invoice-delete-view/<int:pk>/', delete_bill_invoice_view, name='bill_invoice_delete_view'),

    path('billing-category-create-view/<int:pk>/', CreateBillingCategoryView.as_view(), name='billing_category_create_view'),
    path('billing-category-edit-view/<int:pk>/', EditBillingCategoryView.as_view(), name='bill_category_edit_view'),
    path('billing-category-delete-view/<int:pk>/', delete_bill_category_view, name='bill_category_delete_view'),

    # payroll views
    path('payroll/homepage/', PayrollHomepageView.as_view(), name='payroll_homepage'),
    path('payroll/employee-list/', EmployeeListView.as_view(), name='payroll_employee'),
    path('payroll/employee-create/', EmployeeCreateView.as_view(), name='payroll_employee_create'),


    ]