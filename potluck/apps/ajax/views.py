from django.http import JsonResponse

from potlucks.models import Order, CustomerOrder, Wishlist




from users.models import CustomUser


def validate_goods_number(request, pk):
    order = Order.objects.get(id=pk)
    goods_number = request.GET.get('number', None)

    customer_order = CustomerOrder.objects.filter(order=order, customer=request.user.profile)
    print(customer_order.exists())
    if not customer_order.exists():

        max_number = order.size - order.get_order_fullness()
    else:
        max_number = order.size - order.get_order_fullness() + customer_order[0].goods_number

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


def validate_email_to_reset_password(request):
    """Проверка доступности email"""
    email = request.GET.get('email', None)

    response = {
        'exists': CustomUser.objects.filter(email__iexact=email).exists()
    }
    print(response)
    return JsonResponse(response)


def add_product_to_wishlist(request, pk):
    try:

        wishlist = Wishlist.objects.get(customer=request.user.profile)

        wishlist.products.add(pk)

        wishlist.save()
        return JsonResponse({"product": pk}, status=200)
    except Wishlist.DoesNotExist:

        wishlist = Wishlist.objects.create(customer=request.user.profile)
        wishlist.products.add(pk)
        wishlist.save()
        return JsonResponse({"product": pk}, status=200)


def delete_product_from_wishlist(request, pk):


    wishlist = Wishlist.objects.get(customer=request.user.profile)

    wishlist.products.remove(pk)

    wishlist.save()
    return JsonResponse({"product": pk}, status=200)
