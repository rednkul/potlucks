from django import forms
from django.utils.safestring import mark_safe
from users.admin import admin

from django_admin_json_editor import JSONEditorWidget

from .models import Category, Product, ProductImages, Manufacturer, Parameters, Wishlist, Rating, RatingStar, Review

from .utils import parameters_to_data

# Register your models here.


admin.site.site_title = "Администрируй тут"
admin.site.site_header = "Администрируй тут"


class MyModelAdmin(admin.ModelAdmin):
    # Класс для добавления метода вывода изображения
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url if obj.image else None} width="100" height="auto">')

    get_image.short_description = "Изображение"


class CategoryAdmin(MyModelAdmin):
    list_display = ("id", "name", "get_parents", "get_image", "url",)
    list_display_links = ("id", "name", "get_image", "url",)
    list_filters = ("parent__name",)
    search_fields = ("name",)

    @staticmethod
    def get_parents(obj):
        return " > ".join([i.name for i in obj.get_ancestors()])

    get_parents.shot_description = "Предки"


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


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    readonly_fields = ('get_image',)
    extra = 0

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url if obj.image else None} width="100" height="auto">')

    get_image.short_description = "Изображение"


class ProductAdmin(MyModelAdmin):
    form = ProductAdminForm
    list_display = (
        'id', 'name', 'get_image', 'price', 'stock',
        'available', 'manufacturer', 'get_categories',
    )
    list_display_links = ('id', 'name')
    list_filter = ('manufacturer', 'category', 'available')
    search_fields = ('name', 'manufacturer__name', 'category__name')
    save_on_top = True
    readonly_fields = ('created_at', 'updated_at', 'get_image')
    inlines = [ProductImagesInline]
    fieldsets = (
        (None, {
            "fields": (("name", "available", "stock", "price"),)
        }),
        (None, {
            "fields": (("created_at", "updated_at",),)
        }),
        (None, {
            "fields": (("url", "category",),)
        }),
        (None, {
            "fields": (("manufacturer",),), "classes": ("wide",)
        }),
        (None, {
            "fields": (("description", "image", "get_image"),)
        }),
        (None, {
            "fields": (("tags",),)
        }),
        (None, {
            "fields": (("parameters",),)
        }),

    )

    def get_categories(self, obj):
        return " > ".join([i.name for i in obj.category.get_ancestors(include_self=True)]) if obj.category else ''

    get_categories.short_description = "Категории"


class RatingInline(admin.TabularInline):
    model = Rating
    raw_id_fields = ['star']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "date")
    list_display_links = ("customer", "product",)
    list_filter = ("product", "customer",)
    search_fields = ("customer__profile__user__email", "product__name")
    inlines = [RatingInline]


class RatingAdmin(admin.ModelAdmin):
    """Настройка страницы рейтинга"""
    list_display = ("review", "star")
    list_display_links = ("review",)
    list_filter = ("review__customer", "review__product",)
    search_fields = ("review__customer__user__email", "review__product__name",)


class ProductImagesAdmin(MyModelAdmin):
    model = ProductImages
    list_display = ('product', "get_image")
    list_display_links = ('product', "get_image")
    list_filter = ("product",)
    search_fields = ("product__name",)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)
admin.site.register(Parameters)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RatingStar)
admin.site.register(Wishlist)
