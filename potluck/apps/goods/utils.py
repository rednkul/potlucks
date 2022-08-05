from .models import Parameters, Category

def get_parameters_names():
    # Формируется список названий объектов модели Parameters
    return [i for i in Parameters.objects.values_list('name', flat=True)]

def parameters_to_data():
    # Формируется схема json
    DATA_SCHEMA = {
        'properties': {
        },
    }
    # В схему добавляются названия характеристик, значения будут заполнены в админке
    for i in get_parameters_names():
        DATA_SCHEMA['properties'][f'{i}'] = ''

    return DATA_SCHEMA



def format_date(date):

    month_names = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
                   'ноября', 'декабря']
    return f'{date.day} {month_names[date.month - 1]} {date.year} г.'



import csv
import urllib
import datetime
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    options = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    print(options.verbose_name)
    response['Content-Disposition'] = f'attachment; filename={urllib.parse.quote_plus(options.verbose_name_plural)}.csv'
    writer = csv.writer(response)
    fields = [field for field in options.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)

            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Экспорт в CSV'

def get_subcategories_of_categories(categories_ids):
    categories = Category.objects.filter(id__in=[int(i) for i in categories_ids])
    subcategories = Category.objects.none()

    for category in categories:
        subcategories = subcategories | category.get_descendants()

    categories = (categories | subcategories).distinct()

    return categories