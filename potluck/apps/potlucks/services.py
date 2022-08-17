from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Part, Potluck, PartOrder

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
    part = Part.objects.filter(id=pk)
    if part:
        part[0].delete()

    return redirect('users:user_part_orders')

