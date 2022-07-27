from users.admin import admin

from .models import Order, CustomerOrder

# Register your models here.

admin.site.site_title = "Администрируй тут"
admin.site.site_header = "Администрируй тут"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'vendor', 'creator', 'date', 'date_amass', 'number_finished')
    list_display_links = ('id', 'product', 'vendor',)
    list_filter = ('product__name', 'vendor__name',)
    search_fields = ('vendor__name', 'size', 'creator__user__email', 'product__name')
    readonly_fields = ('price', )


class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'goods_number', 'order_size', 'created', 'date_send', 'confirmed', 'paid')
    list_display_links = ('id', 'customer')
    list_filter = ('order__vendor', 'order__product__name')
    search_fields = ('customer__user__email', 'order__product__name',
                     'order__vendor__name',)

    @staticmethod
    def order_size(obj):
        return obj.order.size

    order_size.short_description = ("Товаров в заказе")


admin.site.register(Order, OrderAdmin)
admin.site.register(CustomerOrder, CustomerOrderAdmin)
