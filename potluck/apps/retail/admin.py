from django.contrib import admin

from .models import OrderToRetail, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(OrderToRetail)
class OrderRetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated', 'paid')
    search_fields = ('customer__first_name', 'customer__last_name')
    list_display_links = ('id',)
    list_filter = ('paid', )
    save_on_top = True
    inlines = [OrderItemInline]


