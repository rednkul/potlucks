from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.admin import AdminSite

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile


class MyAdminSite(AdminSite):

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        return app_list


admin.site = MyAdminSite()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'is_staff', 'is_confirmed', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_confirmed', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Разрешения', {'fields': ('is_staff', 'is_confirmed', 'is_active')}),
        ('Группы', {'fields': ('groups',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Group, GroupAdmin)
