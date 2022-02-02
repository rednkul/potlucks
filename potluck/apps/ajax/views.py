from django.http import JsonResponse

from potlucks.models import Order, CustomerOrder

from users.models import CustomUser


def validate_goods_number(request, pk):
    order = Order.objects.get(id=pk)
    max_number = order.size - order.get_order_fullness()

    goods_number = request.GET.get('number', None)

    try:
        goods_number_int = int(goods_number)
    except ValueError:
        goods_number_int = 0

    response = {
        'is_available': max_number >= goods_number_int,
        'available_number': max_number,
        'is_integer': goods_number.isdigit(),
    }
    print(response)
    return JsonResponse(response)



def cancel_customer_order(request, pk):
    customer_order = CustomerOrder.objects.get(id=pk)
    customer_order.delete()

    response = {'is_deleted': True if not CustomerOrder.objects.filter(id=pk).exists() else False}


    return JsonResponse(response)


def validate_email(request):
    """Проверка доступности email"""
    email = request.GET.get('email', None)
    print('КРЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ')
    print(email)
    response = {
        'is_taken': CustomUser.objects.filter(email__iexact=email).exists()
    }
    print(response)
    return JsonResponse(response)


