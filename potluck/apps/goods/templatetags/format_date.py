from django import template

register = template.Library()

@register.simple_tag(name='format_date')
def format_date(date):

    month_names = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
                   'ноября', 'декабря']
    return f'{date.day} {month_names[date.month - 1]} {date.year} г.'