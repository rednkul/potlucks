from django.forms import forms, ModelForm, ModelChoiceField,TextInput, RadioSelect
from .models import Review, Rating, RatingStar, Product


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('text',)


class RatingForm(ModelForm):
    star = ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ['star', ]
