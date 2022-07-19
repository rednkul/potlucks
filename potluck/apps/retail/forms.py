from django import forms
from .models import OrderToRetail


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderToRetail
        fields = [
                    'first_name', 'last_name', 'patronymic', 'phone_number',
                    'email', 'city', 'address', 'post_index', 'notes',
                  ]