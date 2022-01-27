from django.http import JsonResponse
from django.shortcuts import redirect

from .models import CustomerOrder, Order

def join_an_order(request, pk):
    order = Order.objects.get(id=pk)
    goods_number = request.POST.get('number')
    customer_order = CustomerOrder.objects.create(customer=request.user.profile, order=order, goods_number=goods_number)
    return redirect('potlucks:order_detail', pk=pk)



def cancel_customer_order(request, pk):
    customer_order = CustomerOrder.objects.get(id=pk)
    customer_order.delete()

    return redirect('users:profile_detail', pk=request.user.profile.pk)

