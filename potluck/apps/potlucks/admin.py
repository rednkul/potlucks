from users.admin import admin
from goods.utils import export_to_csv

from .models import Potluck, Part, PartOrder

# Register your models here.

admin.site.site_title = "Администрируй тут"
admin.site.site_header = "Администрируй тут"


class PotluckAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'vendor', 'creator', 'date', 'date_amass', 'number_finished')
    list_display_links = ('id', 'product', 'vendor',)
    list_filter = ('product__name', 'vendor__name',)
    search_fields = ('vendor__name', 'size', 'creator__user__email', 'product__name')
    readonly_fields = ('price', )


class PartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'potluck', 'goods_number', 'total_cost', 'potluck_size',
                    'created', 'updated')
    list_display_links = ('id', 'customer')
    list_filter = ('potluck__vendor', 'potluck__product__name')
    search_fields = ('customer__user__email', 'potluck__product__name',
                     'potluck__vendor__name',)

    @staticmethod
    def potluck_size(obj):
        return obj.potluck.size

    @staticmethod
    def total_cost(obj):
        return obj.total_cost

    potluck_size.short_description = ("Товаров в складчине")

class PartOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'part', 'total_cost', 'email', 'phone_number', 'first_name',
                    'created', 'confirmed', 'paid')
    list_display_links = ('id', 'part')
    list_filter = ('part__potluck__vendor', 'part__potluck__product__name')
    search_fields = ('part__customer__user__email', 'part__potluck__product__name',
                     'part__potluck__vendor__name',)
    actions = [export_to_csv]

    @staticmethod
    def potluck_size(obj):
        return obj.part.potluck.size

    @staticmethod
    def total_cost(obj):
        return obj.part.total_cost

admin.site.register(Potluck, PotluckAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(PartOrder, PartOrderAdmin)


