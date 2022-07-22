from django.contrib import admin
from django import forms
from django_admin_json_editor import JSONEditorWidget



from .models import Category, Product, ProductImages, Vendor, Manufacturer, Parameters, Wishlist, Rating, RatingStar, Review

from .utils import parameters_to_data

# Register your models here.

admin.site.site_title = "Администрируй тут"
admin.site.site_header = "Администрируй тут"




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_parents", "image", "url",)
    list_display_links = ("id", "name", "url",)
    list_filters = ("parent__name",)
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
    list_display = ('id', 'name', 'image', 'price', 'stock', 'available', 'manufacturer', 'get_vendors', 'get_categories',)
    list_display_links = ('id', 'name')
    list_filter = ('vendors', 'manufacturer', 'category', 'available')
    search_fields = ('name', 'vendors__name', 'manufacturer__name', 'category__name')
    filter_horizontal = ("vendors", )
    save_on_top = True
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            "fields": (("name", "available", "stock", "price" ), )
        }),
        (None, {
            "fields": (("created_at", "updated_at",),)
        }),
        (None, {
            "fields": (("url", "category",),)
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
        return " > ".join([i.name for i in obj.category.get_ancestors(include_self=True)]) if obj.category else ''


    def get_vendors(self, obj):
         return "\n".join([i.name for i in obj.vendors.all()])


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "date")
    list_display_links = ("customer", "product",)
    list_filter = ("product", "customer",)
    search_fields = ("customer__profile__user__email", "product__name")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Настройка страницы рейтинга"""
    list_display = ("customer", "product", "date")
    list_display_links = ("customer", "product",)
    list_filter = ("product", "customer",)
    search_fields = ("customer__profile__user__email", "product__name")


admin.site.register(RatingStar)
admin.site.register(Parameters)
admin.site.register(ProductImages)
admin.site.register(Wishlist)


