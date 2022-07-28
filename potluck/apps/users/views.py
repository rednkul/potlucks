from allauth.account.forms import ChangePasswordForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView

from .models import Profile, CustomUser
from potlucks.models import Part
from goods.models import Rating, RatingStar



class ProfileDetailView(UpdateView):
    model = Profile
    template_name = 'users/profile_detail.html'
    fields = ['first_name', 'last_name', 'patronymic', 'address', 'phone_number', 'vk', 'telegram', 'post_index', 'city']


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