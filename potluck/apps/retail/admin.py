from users.admin import admin

from goods.utils import export_to_csv
from .models import OrderToRetail, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderRetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated', 'confirmed', 'paid')
    search_fields = ('customer__first_name', 'customer__last_name')
    list_display_links = ('id',)
    list_filter = ('paid',)
    save_on_top = True
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(OrderToRetail, OrderRetailAdmin)
