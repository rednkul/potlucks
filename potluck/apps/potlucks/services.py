from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Part, Potluck

def join_potluck(request, pk):
    potluck = Potluck.objects.get(id=pk)
    goods_number = request.POST.get('number')
    part = Part.objects.create(customer=request.user.profile, potluck=potluck, goods_number=goods_number)
    return redirect('potlucks:potluck_detail', pk=pk)

def update_part(request, pk):
    part = Part.objects.get(id=pk)
    part.goods_number = request.POST.get('number')
    part.save()

    return redirect('potlucks:potluck_detail', pk=part.potluck.id)



def cancel_part(request, pk):
    part = Part.objects.get(id=pk)
    part.delete()

    return redirect('users:profile_detail', pk=request.user.profile.pk)

# def review_and_rate(request, pk):
#
#     review = request.POST.get(f'review{pk}')
#     star = request.POST.get(f"star{pk}")
#     customer_order = CustomerOrder.objects.get(id=pk)
#
#
#     Rating.objects.update_or_create(
#
#         customer_order=customer_order,
#         defaults={'star_id': int(star) if star else 5},
#     )
#
#     if review:
#         Review.objects.update_or_create(
#
#             customer_order=customer_order,
#             text=review,
#         )
#
#     return redirect('users:profile_detail', pk=request.user.profile.id)