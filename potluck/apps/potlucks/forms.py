from django import forms

from .models import PartOrder

class PartOrderCreateForm(forms.ModelForm):
    class Meta:
        model = PartOrder
        fields = [
                    'part', 'first_name', 'last_name', 'patronymic', 'phone_number',
                    'email', 'city', 'address', 'post_index', 'notes',
                  ]