from django.shortcuts import render
from django.views.generic import DetailView, UpdateView

from .models import Profile
from potlucks.models import CustomerOrder

class ProfileDetailView(UpdateView):
    model = Profile
    template_name = 'users/profile_detail.html'
    fields = ['phone_number', 'instagram', 'vk', 'telegram', 'post_index']


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        customer_orders_active = CustomerOrder.objects.filter(customer=customer, order__finished=False)
        customer_orders_finished = CustomerOrder.objects.filter(customer=customer, order__finished=True)
        context['customer_orders_active'] = customer_orders_active
        context['customer_orders_finished'] = customer_orders_finished

        return context