from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from users.models import Profile, CustomUser

from .models import OrderToRetail, OrderItem
from goods.utils import format_date
from users.services import across_registration_and_login
from users.mixins import GroupRequiredMixin
from send_notification.views import send_order_notification

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
                across_registration_and_login(order, request)
            send_order_notification(order)
            return redirect('retail:order_created', order_id=order.id)

    else:
        form = OrderCreateForm
    return render(request, 'retail/orders/order_create.html',
                  {'cart': cart, 'form': form})


def order_created(request, order_id):
    order = get_object_or_404(OrderToRetail, id=order_id)
    return render(request, 'retail/orders/order_created.html', {'order': order})


class OrderListView(GroupRequiredMixin, ListView):
    group_required = ['Manager', ]
    queryset = OrderToRetail.objects.all().order_by('-created')
    context_object_name = 'orders'
    template_name = 'retail/orders/orders.html'
    paginate_by = 4
    paginate_orphans = 3


class OrderFilterListView(GroupRequiredMixin, ListView):
    group_required = ['Manager', ]
    context_object_name = 'orders'
    template_name = 'retail/orders/orders.html'
    paginate_by = 4
    paginate_orphans = 3

    def get_queryset(self):
        get_confirmed = self.request.GET.getlist("confirmed")
        get_paid = self.request.GET.getlist("paid")
        request = self.request.GET.get('order_search')

        confirmed_filter = get_confirmed if get_confirmed else (True, False)
        paid_filter = get_paid if get_paid else (True, False)

        queryset = OrderToRetail.objects.filter(
            confirmed__in=confirmed_filter,
            paid__in=paid_filter
        ).order_by('-created')

        if request:

            if request.isdigit():
                queryset = queryset.filter(
                    Q(id__exact=request) |
                    Q(phone_number__exact=request) |
                    Q(post_index__exact=request)
                )

            else:
                queryset = queryset.filter(
                    Q(email__contains=request) |
                    Q(notes__iregex=request) |
                    Q(first_name__iregex=request) |
                    Q(last_name__iregex=request) |
                    Q(patronymic__iregex=request) |
                    Q(city__iregex=request) |
                    Q(address__iregex=request)
                )


        return queryset

    def get_context_data(self, *args, **kwargs):
        get_confirmed = self.request.GET.getlist("confirmed")
        get_paid = self.request.GET.getlist("paid")
        search = self.request.GET.get('order_search')

        context = super().get_context_data(*args, **kwargs)

        context['confirmed'] = get_confirmed
        context['paid'] = get_paid

        context['q'] = f"q={search}&"
        context['orders_search'] = search
        return context

class JsonOrderFilterListView(GroupRequiredMixin, ListView):
    group_required = ['Manager', ]
    context_object_name = 'orders'
    paginate_orphans = 3

    def get_paginate_by(self):
        return 5

    def get_queryset(self):
        get_confirmed = self.request.GET.getlist("confirmed")
        get_paid = self.request.GET.getlist("paid")
        request = self.request.GET.get('order_search')

        confirmed_filter = get_confirmed if get_confirmed else (True, False)
        paid_filter = get_paid if get_paid else (True, False)

        queryset = OrderToRetail.objects.filter(
            confirmed__in=confirmed_filter,
            paid__in=paid_filter
        ).order_by('-created')

        if request:

            if request.isdigit():
                queryset = queryset.filter(
                    Q(id__exact=request) |
                    Q(phone_number__exact=request) |
                    Q(post_index__exact=request)
                ).distinct()

            else:
                queryset = queryset.filter(
                    Q(email__contains=request) |
                    Q(notes__iregex=request) |
                    Q(first_name__iregex=request) |
                    Q(last_name__iregex=request) |
                    Q(patronymic__iregex=request) |
                    Q(city__iregex=request) |
                    Q(address__iregex=request)
                ).distinct()

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = {'paginate_by': self.get_paginate_by(), 'orders': {}}
        for order in queryset:
            response['orders'][f'{order.id}'] = {
                'customer': str(order.customer.id) if order.customer else '',
                'first_name': order.first_name,
                'last_name': order.last_name,
                'patronymic': order.patronymic,
                'phone_number': str(order.phone_number),
                'email': order.email,
                'city': order.city,
                'address': order.address,
                'post_index': str(order.post_index),
                'notes': order.notes,
                'created': format_date(order.created),
                'total_cost': str(order.get_total_cost),
                'items': {},
                'confirmed': order.confirmed,
                'paid': order.paid,


            }
            for item in order.items.all():
                response['orders'][f'{order.id}']['items'][f'{item.id}'] = {
                    'product': item.product.name,
                    'quantity': str(item.quantity),
                    'price': str(item.product.price),
                    'item_cost': str(item.get_cost),
                }

        return JsonResponse(response, safe=False, status=200)


