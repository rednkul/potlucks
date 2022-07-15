from django.contrib import admin
from django import forms
from django_admin_json_editor import JSONEditorWidget



from .models import Category, Vendor, Manufacturer, Order, CustomerOrder, Rating, Review, Product, ProductImages, \
    RatingStar, Wishlist, Parameters
from .utils import parameters_to_data

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

        return " > ".join([i.name for i in obj.get_ancestors()])





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



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer_order", "date")
    list_display_links = ("customer_order",)
    list_filter = ("customer_order__order__product", "customer_order__order__vendor")
    search_fields = ("customer_order__customer__profile__user__email",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Настройка страницы рейтинга"""
    list_display = ("customer_order", "date")
    list_display_links = ("customer_order",)


admin.site.register(RatingStar)



class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {
            'parameters': JSONEditorWidget(parameters_to_data(), collapsed=True)
        }
        fields = '__all__'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
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
        (None, {
            "fields": (("parameters",), )
        }),

                )



    def get_categories(self, obj):
        return " > ".join([i.name for i in obj.category.get_ancestors(include_self=True)])


    def get_vendors(self, obj):
         return "\n".join([i.name for i in obj.vendors.all()])



admin.site.register(Parameters)
admin.site.register(ProductImages)
admin.site.register(Wishlist)

#class ProductImagesAdmin(admin.ModelAdmin):
