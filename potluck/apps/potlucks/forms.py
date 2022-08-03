from django import forms

from .models import PartOrder, Potluck


class PartOrderCreateForm(forms.ModelForm):
    class Meta:
        model = PartOrder
        fields = [
            'part', 'first_name', 'last_name', 'patronymic', 'phone_number',
            'email', 'city', 'address', 'post_index', 'notes',
        ]


class PotluckCreateForm(forms.ModelForm):
    class Meta:
        model = Potluck
        fields = ['product', 'creator', 'vendor', 'size', 'unit_price']
