from django.http import JsonResponse
from django.shortcuts import redirect

from .models import CustomerOrder, Order

def join_an_order(request, pk):
    order = Order.objects.get(id=pk)
    goods_number = request.POST.get('number')
    customer_order = CustomerOrder.objects.create(customer=request.user.profile, order=order, goods_number=goods_number)
    return redirect('potlucks:order_detail', pk=pk)



def validate_goods_number(request, pk):
    order = Order.objects.get(id=pk)
    max_number = order.size - order.get_order_fullness()
    goods_number = request.GET.get('number')
    response = {'is_available': True if max_number >= goods_number else False}
    return JsonResponse(response)

