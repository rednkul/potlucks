from django.forms import forms, ModelForm, ModelChoiceField,TextInput, RadioSelect
from .models import Review, Rating, RatingStar, Product


class ReviewForm(ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Review
        fields = ('text',)


class RatingForm(ModelForm):
    """Форма рейтинга"""
    star = ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ['star', ]

# class AddProductForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'category', 'vendors', 'manufacturer', 'description',
#                   'tags', 'url', 'available', 'stock','price', 'image'
#                   ]
#         widgets = {
#             'name': TextInput(attrs={'class': 'check-input'}),
#
#
#         }

    # def get_wigets(self):
    #     wigets = {}
    #     for field in self._meta.fields:
    #         if field.
