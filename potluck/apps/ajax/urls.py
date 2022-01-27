from django.urls import path
from . import views

app_name = 'ajax'

urlpatterns = [
    path('validate_goods_number/<int:pk>/', views.validate_goods_number, name='validate_goods_number'),

]