from django.urls import path
from .views import (
    WarehouseDashboard, BillingHomepageView, BillingStoreListView,
    CreateBillingInvoiceView, BillInvoiceEditView, quick_billing_pay,
    delete_bill_invoice_view, CreateBillingCategoryView, EditBillingCategoryView, delete_bill_category_view,
    )
from .invoice_views import (WarehouseOrderList, create_warehouse_order_view, UpdateWarehouseOrderView,
                            CreateOrderItem, create_or_add_order_item, UpdateInvoiceOrderItem,
                            delete_warehouse_order_item_view,
                            VendorListView, VendorCreateView, VendorUpdateView, delete_vendor,
                            CreateInvoiceImageView, UpdateInvoiceImageView, delete_invoice_image_view,
                            PaycheckCreateView, PayCheckListView, PaycheckDetailView, delete_paycheck,
                            create_payment_from_order_view
                            )

from .payroll_views import (PayrollHomepageView, EmployeeListView, EmployeeCreateView, EmployeeEditView, delete_employee,
                            OccupationCreateView, OccupationListView, OccupationUpdateView, delete_occupation, EmployeeListCardView,
                            PayrollCreateView, EmployeeCardView, payroll_quick_pay, PayrollUpdateView, delete_payroll
                            )
from .ajax_calls import ajax_paycheck_actions, ajax_calculate_value

app_name = 'warehouse'

urlpatterns = [
    path('', WarehouseDashboard.as_view(), name='dashboard'),

    # invoices
    path('invoices/', WarehouseOrderList.as_view(), name='invoices'),
    path('create-invoice/', create_warehouse_order_view, name='create_invoice'),
    path('invoices/update/<int:pk>/', UpdateWarehouseOrderView.as_view(), name='update_order'),
    path('invoice/order-item/check/<int:pk>/<int:dk>/', create_or_add_order_item, name='order_item_check'),
    path('invoice/order-item/create/<int:pk>/<int:dk>/', CreateOrderItem.as_view(), name='create-order-item'),
    path('invoices/order-item/update/<int:pk>/', UpdateInvoiceOrderItem.as_view(), name='order-item-update'),
    path('invoices/order-item/delete/<int:pk>/', delete_warehouse_order_item_view, name='order-item-delete'),
    path('invoices/create-payment-order/<int:pk>/', create_payment_from_order_view, name='create-payment-order'),

    # ajax urls
    path('ajax/calculate/<slug:question>/', ajax_calculate_value, name='ajax_invoice'),
    path('ajax/paycheck-actions/<slug:question>/', ajax_paycheck_actions, name='ajax_paycheck_actions'),


    path('invoice/order-image/create/<int:pk>/', CreateInvoiceImageView.as_view(), name='create-order-image'),
    path('invoices/order-image/update/<int:pk>/', UpdateInvoiceImageView.as_view(), name='update-order-image'),
    path('invoices/order-image/delete/<int:pk>/', delete_invoice_image_view, name='delete-order-image'),

    path('paychecks/', PayCheckListView.as_view(), name='paychecks'),
    path('paychecks/<int:pk>/', PaycheckDetailView.as_view(), name='paycheck_detail'),
    path('paychecks/create/', PaycheckCreateView.as_view(), name='paycheck_create'),
    path('paychecks/delete/<int:pk>/', delete_paycheck, name='paycheck_delete'),


    path('vendors/', VendorListView.as_view(), name='vendors'),
    path('vendor/<int:pk>/', VendorUpdateView.as_view(), name='vendor_detail'),
    path('vendors/create/', VendorCreateView.as_view(), name='vendor_create'),
    path('vendor/delete/<int:pk>/', delete_vendor, name='vendor_delete'),

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
    path('payroll/employee-card/', EmployeeListCardView.as_view(), name='employee-card-list'),
    path('payroll/employee-list/', EmployeeListView.as_view(), name='payroll_employee'),
    path('payroll/employee-create/', EmployeeCreateView.as_view(), name='payroll_employee_create'),
    path('payroll/employee-edit/<int:pk>/', EmployeeEditView.as_view(), name='payroll_employee_edit'),
    path('payroll/employee-delete/<int:pk>/', delete_employee, name='payroll_employee_delete'),

    path('payroll/occupation-list/', OccupationListView.as_view(), name='occupation_list'),
    path('payroll/occupation-create/', OccupationCreateView.as_view(), name='occupation_create'),
    path('payroll/occupation-edit/<int:pk>/', OccupationUpdateView.as_view(), name='occupation_edit'),
    path('payroll/occupation-delete/<int:pk>/', delete_occupation, name='occupation_delete'),

    path('payroll/create/<int:pk>/', PayrollCreateView.as_view(), name='employee_create_payroll'),
    path('payroll/employee-card-detail/<int:pk>/', EmployeeCardView.as_view(), name='employee-card-detail'),
    path('payroll/quick-pay/<int:pk>/', payroll_quick_pay, name='payroll_quick_pay'),
    path('payroll/edit/<int:pk>/', PayrollUpdateView.as_view(), name='payroll_edit'),
    path('payroll/delete/<int:pk>/', delete_payroll, name='payroll_delete'),

    ]