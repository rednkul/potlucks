from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from potlucks.models import Potluck, Part

from goods.models import Wishlist, Product

from users.models import CustomUser

from users.services import user_check_group


def validate_goods_number(request, pk):
    """
    Validation of quantity of goods in potluck form
    """
    potluck = Potluck.objects.get(id=pk)
    goods_number = request.GET.get('number', None)

    part = Part.objects.filter(potluck=potluck, customer=request.user.profile)

    if not part.exists():

        max_number = potluck.size - potluck.get_potluck_fullness()
    else:
        max_number = potluck.size - potluck.get_potluck_fullness() + part[0].goods_number

    try:
        goods_number_int = int(goods_number)
    except ValueError:
        goods_number_int = 0

    response = {
        'sum': goods_number_int * potluck.unit_price,
        'is_available': max_number >= goods_number_int,
        'available_number': max_number,
        'is_integer': goods_number.isdigit(),
    }

    return JsonResponse(response)


def cancel_part(request, pk):
    """
    Cancellation of a partnership in potluck
    """
    part = Part.objects.get(id=pk)
    if user_check_group(request.user, 'Manager') or part.customer.user == request.user:
        part.delete()
    else:
        raise PermissionDenied
    response = {'is_deleted': True if not Part.objects.filter(id=pk).exists() else False}

    return JsonResponse(response)


def validate_email(request):
    """

    """
    email = request.GET.get('email', None)

    response = {
        'exists': CustomUser.objects.filter(email__iexact=email).exists()
    }

    return JsonResponse(response)



def add_product_to_wishlist(request, pk):
    wishlist = Wishlist.objects.get(customer=request.user.profile)

    wishlist.products.add(pk)

    wishlist.save()

    response = {"product": pk, "wishlist_qty": wishlist.products.count()}


    return JsonResponse(response, status=200)


def product_make_available(request, pk):
    product = Product.objects.get(pk=pk)

    product.available = True

    product.save()

    response = {"product": pk, "success": True}

    return JsonResponse(response, status=200)


def product_make_unavailable(request, pk):
    if not user_check_group(request.user, 'Manager') :
        raise PermissionDenied
    product = Product.objects.get(pk=pk)

    product.available = False

    product.save()

    response = {"product": pk, "success": True}

    return JsonResponse(response, status=200)


def delete_product_from_wishlist(request, pk):
    wishlist = Wishlist.objects.get(customer=request.user.profile)

    wishlist.products.remove(pk)

    wishlist.save()

    response = {"product": pk, "wishlist_qty": wishlist.products.count()}


    return JsonResponse(response, status=200)
