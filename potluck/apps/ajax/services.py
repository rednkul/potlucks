from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from retail.models import OrderToRetail
from potlucks.models import PartOrder

from users.services import user_check_group


def confirm_order(request, pk, order_type):
    """
    After the customer creates an order, the manager contacts the customer and confirms the order
    """
    if not user_check_group(request.user, 'Manager'):
        raise PermissionDenied
    order = OrderToRetail.objects.get(id=pk) if order_type == 'retail' else PartOrder.objects.get(id=pk)
    order.confirmed = True
    order.save()
    response = {'order': pk, 'message': 'Заказ подтвержден', 'type': order_type}

    return JsonResponse(response, status=200)


def disconfirm_order(request, pk, order_type):
    """
    Cancellation of a confirmed order
    """
    if not user_check_group(request.user, 'Manager'):
        raise PermissionDenied
    order = OrderToRetail.objects.get(id=pk) if order_type == 'retail' else PartOrder.objects.get(id=pk)
    order.confirmed = False
    order.save()
    response = {'order': pk, 'message': 'Заказ отменен', 'type': order_type}

    return JsonResponse(response, status=200)


def paid_order(request, pk, order_type):
    """
    After the order is paid, the manager sets this flag
    """
    if not user_check_group(request.user, 'Manager'):
        raise PermissionDenied
    order = OrderToRetail.objects.get(id=pk) if order_type == 'retail' else PartOrder.objects.get(id=pk)
    order.paid = True
    order.save()
    response = {'order': pk, 'message': 'Заказ оплачен', 'type': order_type}
    return JsonResponse(response, status=200)


def unpaid_order(request, pk, order_type):
    """
    Cancellation of a paid order
    """
    if not user_check_group(request.user, 'Manager'):
        raise PermissionDenied
    order = OrderToRetail.objects.get(id=pk) if order_type == 'retail' else PartOrder.objects.get(id=pk)
    order.paid = False
    order.save()
    response = {'order': pk, 'message': 'Оплата отменена', 'type': order_type}
    return JsonResponse(response, status=200)

def delete_order(request, pk, order_type):
    if not user_check_group(request.user, 'Manager'):
        raise PermissionDenied
    order = OrderToRetail.objects.get(id=pk) if order_type == 'retail' else PartOrder.objects.get(id=pk)
    order.delete()
    response = {'order': pk, 'message': 'Заказ удален', 'type': order_type}
    return JsonResponse(response, status=200)