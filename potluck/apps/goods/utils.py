from .models import Parameters

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
