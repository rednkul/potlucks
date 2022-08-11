from django.http import JsonResponse

from retail.models import OrderToRetail as Order

def confirm_order(request, pk):
    print(f'---------------------{pk}')
    order = Order.objects.get(id=pk)
    order.confirmed = True
    order.save()
    response = {'order': pk, 'message': 'Заказ подтвержден'}
    print(response)
    return JsonResponse(response, status=200)

def disconfirm_order(request, pk):
    print(f'---------------------{pk}')
    order = Order.objects.get(id=pk)
    order.confirmed = False
    order.save()
    response = {'order': pk, 'message': 'Заказ отменен'}
    print(response)
    return JsonResponse(response, status=200)


