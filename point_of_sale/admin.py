from django.contrib import admin

from .models import OrderItemAttribute, OrderItem


@admin.register(OrderItemAttribute)
class OrderItemAttrAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass