from django.http import JsonResponse

from potlucks.models import Order, CustomerOrder




def validate_goods_number(request, pk):
    order = Order.objects.get(id=pk)
    max_number = order.size - order.get_order_fullness()

    goods_number = request.GET.get('number', None)

    try:
        goods_number_int = int(goods_number)
    except ValueError:
        goods_number_int = 0

    response = {
        'is_available': True if max_number >= goods_number_int else False,
        'available_number': max_number,
        'is_integer': True if goods_number.isdigit() else False,
    }
    print(response)
    return JsonResponse(response)

# def finish_order(request, pk):
#     order = Order.objects.get(id=pk)
#     print(order.get_order_fullness(), '----------------', order.size )
#     if order.get_order_fullness() == order.size:
#         order.finished = True
#         order.number_finished += 1
#         response = {
#             'is_finished': True
#         }
#     else:
#         response = {
#             'is_finished': False
#         }
#     print(response)
#     return JsonResponse(response)

def cancel_customer_order(request, pk):
    customer_order = CustomerOrder.objects.get(id=pk)
    customer_order.delete()

    response = {'is_deleted': True if not CustomerOrder.objects.filter(id=pk).exists() else False}
    print('КРЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ')

    return JsonResponse(response)


