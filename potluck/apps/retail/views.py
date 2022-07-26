from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from users.models import Profile, CustomUser

from .models import OrderToRetail, OrderItem
from users.services import across_registration


from cart.cart import Cart
from .forms import OrderCreateForm




def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )

            # очистка корзины
            cart.clear()
            # Если email не принадлежит уже зарегистрированному пользователю,
            # по данным заказа создается новый пользователь со случайным паролем
            if order.email not in CustomUser.objects.values_list('email', flat=True):
                across_registration(order)
            return redirect('retail:order_created', order_id=order.id)
    else:
        form = OrderCreateForm
    return render(request, 'retail/orders/order_create.html',
                  {'cart': cart, 'form': form})


def order_created(request, order_id):
    return render(request, 'retail/orders/order_created.html', {'order': order_id})




