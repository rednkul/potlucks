from django import template

from goods.models import Review

register = template.Library()

@register.simple_tag(name='is_reviewed_by_user')
def is_reviewed_by_user(product_id, profile_id):
    return Review.objects.filter(product=product_id, customer=profile_id).exists()

@register.simple_tag(name='user_review')
def user_review(product_id, profile_id):
    if is_reviewed_by_user(product_id, profile_id):
        return Review.objects.get(product=product_id, customer=profile_id).text
    else:
        return ''