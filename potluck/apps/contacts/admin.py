from users.admin import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from .models import PhoneNumber, Address, Email, CustomFlatPage, AboutUs



class EmailAdmin(admin.ModelAdmin):
    list_display = ('role', 'email')
    list_display_links = ('role', 'email')



class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('role', 'format_number')
    list_display_links = ('role', 'format_number')



class AddressAdmin(admin.ModelAdmin):
    list_display = ('role', 'name')
    list_display_links = ('role', 'name')


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('role', )
    list_display_links = ('role', )

class CustomFlatPageInline(admin.StackedInline):
    model = CustomFlatPage
    verbose_name = "Содержание"


class CustomFlatPageAdmin(FlatPageAdmin):
    inlines = [CustomFlatPageInline]
    fieldsets = (
        (None, {'fields': ('url', 'title', 'sites')}),
        (('Advanced options'), {
            'fields': ('template_name',),
        }),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')

admin.site.register(Address, AddressAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(AboutUs, AboutUsAdmin)


admin.site.register(FlatPage, CustomFlatPageAdmin)