from django.contrib import admin
from .models import Category, Vendor, Manufacturer, Order, CustomerOrder, Rating, Reviews, Product, ProductImages

# Register your models here.

admin.site.site_title = "Администрируй тут"
admin.site.site_header = "Администрируй тут"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_parents", "image", "url",)
    list_display_links = ("id", "name", "url",)
    list_filters = ("parent__name")
    search_fields = ("name",)

    def get_parents(self, obj):
        # return "\n".join([i.name for i in obj.categories.all()])
        if obj.parent:
            parent = obj.parent
            ancestors = [parent.name, ]
            while parent.parent:
                ancestors.append(parent.parent.name)
                parent = parent.parent

            return " > ".join([i for i in ancestors])





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
    list_display = ('id', 'product', 'size', 'vendor', 'creator', 'date', 'date_amass', 'number_finished')
    list_display_links = ('id', 'product', 'vendor',)
    list_filter = ('product__name', 'vendor__name',)
    search_fields = ('vendor__name', 'size', 'creator__user__email', 'product__name')
    readonly_fields = ('price', )





@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'goods_number', 'order_size', 'date')
    list_display_links = ('id', 'customer')
    list_filter = ('order__vendor', 'order__product__name')
    search_fields = ('customer__user__email', 'order__product__name',
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



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'manufacturer', 'get_vendors', 'get_categories',)
    list_display_links = ('id', 'name')
    list_filter = ('vendors', 'manufacturer', 'category')
    search_fields = ('name', 'vendors__name', 'manufacturer__name', 'category__name')
    filter_horizontal = ("vendors", )
    save_on_top = True
    fieldsets = (
        (None, {
            "fields": (("name", "url", "category"), )
        }),
        (None, {
            "fields": (("vendors", "manufacturer", ), ),  "classes": ("wide",)
        }),
        (None, {
            "fields": (("description", "image"),)
        }),
        (None, {
            "fields": (("tags",),)
        }),
        ('Общие характеристики', {
            "fields": ("colors", "materials",), "classes": ("collapse",)
        }),
        ('Характеристики для одежды', {
            "fields": ("sizes_eu", "sizes_am"), "classes":("collapse",)
        }),
                )
    def get_categories(self, obj):
        # return "\n".join([i.name for i in obj.categories.all()])
        if obj.category:
            category = obj.category
            categories = [category.name, ]
            while category.parent:
                categories.append(category.parent.name)
                category = category.parent

            return " > ".join([i for i in categories])


    def get_vendors(self, obj):
         return "\n".join([i.name for i in obj.vendors.all()])


admin.site.register(ProductImages)

#class ProductImagesAdmin(admin.ModelAdmin):
