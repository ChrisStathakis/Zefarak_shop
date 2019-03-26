from django.conf import settings


def dashboard(request):
    page_name = 'Admin Demo Site'
    warehouse_transacations = settings.WAREHOUSE_ORDERS_TRANSCATIONS
    return {
        'page_name': page_name,
        'warehouse_transations': warehouse_transacations
    }