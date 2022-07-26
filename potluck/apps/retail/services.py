# -*- coding: cp1251 -*-

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

