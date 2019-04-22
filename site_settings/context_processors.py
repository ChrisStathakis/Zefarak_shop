from django.conf import settings
import datetime


def dashboard(request):
    page_name = 'Admin Demo Site'
    warehouse_transacations = settings.USE_WAREHOUSE
    date_start, date_end = datetime.datetime(datetime.datetime.now().year, 1, 1).date(), datetime.datetime(datetime.datetime.now().year, 12, 31)
    date_end = datetime.datetime.strftime(date_end, '%m/%d/%Y')
    date_start = datetime.datetime.strftime(date_start, '%m/%d/%Y')
    return {
        'page_name': page_name,
        'warehouse_transations': warehouse_transacations,
        'date_start': date_start,
        'date_end': date_end
    }