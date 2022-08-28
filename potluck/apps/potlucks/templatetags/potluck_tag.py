from django import template

from potlucks.models import Potluck

register = template.Library()


@register.inclusion_tag('potlucks/tags/most_amass_potlucks.html')
def get_most_amass_potlucks(count=5):
    """Вывод 5 заказов с наибольшим процентом заполненности"""
    potlucks = Potluck.objects.filter(amassed=False)
    potlucks = sorted(potlucks, key=lambda x: x.get_potluck_fullness() / x.size, reverse=True)[:count]
    return {'most_amass_potlucks': potlucks}
