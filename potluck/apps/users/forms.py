from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ProfileChangeForm(forms.Form):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'patronymic', 'address', 'phone_number', 'instagram', 'vk', 'telegram',
                  'post_index']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Имя',
            'patronymic': 'Имя',
            'address': 'Имя',
            'phone_number': 'Имя',
            'instagram': 'Имя',
            'vk': 'Имя',
            'telegram': 'Имя',
            'post_index': 'Имя',

        }
