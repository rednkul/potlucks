from allauth.account.forms import ChangePasswordForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, ListView

from .models import Profile, CustomUser
from potlucks.models import Part, Potluck, PartOrder
from goods.models import Rating, RatingStar
from retail.models import OrderToRetail


class ProfileDetailView(UpdateView):
    model = Profile
    template_name = 'users/profile_detail.html'
    fields = ['first_name', 'last_name', 'patronymic', 'address', 'phone_number', 'vk', 'telegram', 'post_index',
              'city']

    def get_object(self, queryset=None):
        return Profile.objects.get(id=self.request.user.profile.id)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        parts_active = Part.objects.filter(customer=customer, potluck__amassed=False)
        parts_amassed = Part.objects.filter(customer=customer, potluck__amassed=True, confirmed_by_user=False)
        parts_confirmed = Part.objects.filter(customer=customer, confirmed_by_user=True)

        context['stars'] = RatingStar.objects.all()
        context['parts_active'] = parts_active
        context['parts_amassed'] = parts_amassed
        context['parts_confirmed'] = parts_confirmed

        return context


class UserOrdersListView(ListView):
    context_object_name = 'orders'
    template_name = 'users/user_orders/user_orders.html'
    paginate_by = 5
    paginate_orphans = 2

    def get_queryset(self):
        return OrderToRetail.objects.filter(customer=self.request.user.profile.id)


class UserPartsListView(ListView):
    context_object_name = 'parts'
    template_name = 'users/user_parts/user_parts.html'
    paginate_by = 5
    paginate_orphans = 2

    def get_queryset(self):
        return Part.objects.filter(customer=self.request.user.profile.id)


class UserPartOrdersListView(ListView):
    context_object_name = 'orders'
    template_name = 'users/user_parts/user_part_orders.html'
    paginate_by = 5
    paginate_orphans = 2

    def get_queryset(self):
        return PartOrder.objects.filter(part__customer=self.request.user.profile.id)
