from django.contrib import admin

from .models import CategoryToRetail, ProductToRetail, ProductImages, OrderToRetail, OrderItem


@admin.register(CategoryToRetail)
class CategoryRetailAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_parents", "image", "url",)
    list_display_links = ("id", "name", "url",)
    list_filters = ("parent__name")
    search_fields = ("name",)

    def get_parents(self, obj):

        return " > ".join([i.name for i in obj.get_ancestors()])


@admin.register(ProductToRetail)
class ProductRetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'get_categories', 'manufacturer',)
    list_display_links = ('id', 'name')
    list_filter = ('category', 'manufacturer',)
    search_fields = ('name', 'category__name', 'manufacturer__name',)
    save_on_top = True
    fieldsets = (
        (None, {
            "fields": (("name", "price", "url", "category"), )
        }),
        (None, {
            "fields": (("description", "image"),)
        }),
        (None, {
            "fields": (("manufacturer",),)
        }),

        (None, {
            "fields": (("tags",),)
        }),

                )

    def get_categories(self, obj):
        return " > ".join([i.name for i in obj.category.get_ancestors(include_self=True)])



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


