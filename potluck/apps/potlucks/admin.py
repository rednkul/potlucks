from django.contrib import admin
from .models import Category, Vendor, Manufacturer, Order, CustomerOrder, Rating, Reviews


# Register your models here.

admin.site.site_title = "Администрируй тут"
admin.site.site_header = "Администрируй тут"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url",)
    list_display_links = ("id", "name", "url",)
    search_fields = ("name",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    list_display_links = ('id', 'name')
    search_fields = ("name",)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    list_display_links = ('id', 'name')
    search_fields = ("name",)




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','vendor', 'size', 'date', 'date_amass', 'number_finished')
    list_display_links = ('id',)
    list_filter = ('vendor__name',)
    search_fields = ('vendor__name',
                      'size')





@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'goods_number', 'order_size', 'date')
    list_display_links = ('id', 'customer')
    list_filter = ('order__vendor',)
    search_fields = ('customer__user__email',
                     'order__vendor__name',)

    def order_size(self, obj):
        return obj.order.size



@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('author', "order", "date")
    list_display_links = ('author', "order",)
    list_filter = ("order",)
    search_fields = ('author', )
#
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Настройка страницы рейтинга"""
    list_display = ("id", "author", "rate", "order",)
    list_display_links = ("id", "author")
    list_filter = ("order",)
    search_fields = ("author__email",)


