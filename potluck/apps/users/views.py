from allauth.account.forms import ChangePasswordForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView

from .models import Profile, CustomUser
from potlucks.models import CustomerOrder

class ProfileDetailView(UpdateView):
    model = Profile
    template_name = 'users/profile_detail.html'
    fields = ['first_name', 'last_name', 'patronymic', 'address', 'phone_number', 'instagram', 'vk', 'telegram', 'post_index']


    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        customer_orders_active = CustomerOrder.objects.filter(customer=customer, order__amassed=False)
        customer_orders_amassed = CustomerOrder.objects.filter(customer=customer, order__amassed=True)
        context['customer_orders_active'] = customer_orders_active
        context['customer_orders_amassed'] = customer_orders_amassed
        print(customer_orders_amassed)

        return context


# class UserChangePasswordView(UpdateView):
#     model = CustomUser
#     fields = ['password', ]
#     template_name = 'users/change_password.html'


def change_password(request):
    u = CustomUser.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = request.POST.get("old_password")
            new_pass = request.POST.get("new_password")
            new_pass_rep = request.POST.get("new_password_repeat")
            if check_password(old_password, u.password):
                return HttpResponse('Пароль успешно изменен')
            else:
                return HttpResponse('bad')
    else:
            form = ChangePasswordForm()

    return render(request, 'users/change_password.html',
              {'form': form, 'user': u})


# def change_password(request, profile_pk):
#     user = Profile.objecst.get(id=profile_pk).user
#     password = request.POST.get('password')
#     user.password = password
#     user.save()