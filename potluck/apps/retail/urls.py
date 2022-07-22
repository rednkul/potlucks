from django.urls import path

from . import views

app_name = 'retail'

urlpatterns = [
    path('order_create/', views.order_create, name='order_create'),
    path('order_created/<int:order_id>/', views.order_created, name='order_created'),

]