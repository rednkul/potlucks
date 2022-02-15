from django.http import JsonResponse
from django.shortcuts import redirect

from .models import CustomerOrder, Order, Rating, Review

def join_an_order(request, pk):
    order = Order.objects.get(id=pk)
    goods_number = request.POST.get('number')
    customer_order = CustomerOrder.objects.create(customer=request.user.profile, order=order, goods_number=goods_number)
    return redirect('potlucks:order_detail', pk=pk)

def update_customer_order(request, pk):
    customer_order = CustomerOrder.objects.get(id=pk)
    customer_order.goods_number = request.POST.get('number')
    customer_order.save()

    return redirect('potlucks:order_detail', pk=customer_order.order.id)



def cancel_customer_order(request, pk):
    customer_order = CustomerOrder.objects.get(id=pk)
    customer_order.delete()

    return redirect('users:profile_detail', pk=request.user.profile.pk)

def review_and_rate(request, pk):

    review = request.POST.get(f'review{pk}')
    star = request.POST.get(f"star{pk}")
    customer_order = CustomerOrder.objects.get(id=pk)


    Rating.objects.update_or_create(

        customer_order=customer_order,
        defaults={'star_id': int(star) if star else 5},
    )

    if review:
        Review.objects.update_or_create(

            customer_order=customer_order,
            text=review,
        )

    return redirect('users:profile_detail', pk=request.user.profile.id)