from django.contrib import admin

# Register your models here.
from .models import PantsProduct, WatchProduct


@admin.register(PantsProduct)
class PantsProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'manufacturer', 'get_vendors', 'get_categories',)
    list_display_links = ('id', 'name')
    list_filter = ('vendors', 'manufacturer', 'categories')
    search_fields = ('name', 'vendors__name', 'manufacturer__name')

    def get_categories(self, obj):
        return "\n".join([i.title for i in obj.categories.all()])

    def get_vendors(self, obj):
         return "\n".join([i.name for i in obj.vendors.all()])


@admin.register(WatchProduct)
class WatchProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'manufacturer', 'get_vendors', 'get_categories',)
    list_display_links = ('id', 'name')
    list_filter = ('vendors', 'manufacturer', 'categories')
    search_fields = ('name', 'vendors__name', 'manufacturer__name')

    def get_categories(self, obj):
        return "\n".join([i.title for i in obj.categories.all()])

    def get_vendors(self, obj):
         return "\n".join([i.name for i in obj.vendors.all()])