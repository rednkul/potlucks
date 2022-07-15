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