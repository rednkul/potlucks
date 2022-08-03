from django.forms import forms, ModelForm, ModelChoiceField,TextInput, RadioSelect



from .models import Review, Rating, RatingStar, Product
from .utils import parameters_to_data

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
#                   'tags', 'url', 'available', 'stock', 'price', 'image', 'parameters'
#                   ]
#         widgets = {
#             'parameters': JSONEditorWidget,
#         }

    # def get_wigets(self):
    #     wigets = {}
    #     for field in self._meta.fields:
    #         if field.


# class ProductAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         widgets = {
#             'parameters': JSONEditorWidget(parameters_to_data(), collapsed=True)
#         }
#         fields = '__all__'