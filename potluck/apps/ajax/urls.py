from django.urls import path
from .views import validate_goods_number

app_name = 'ajax'

urlpatterns = [
    path('validate_goods_number/<int:pk>/', validate_goods_number, name='validate_goods_number'),
    #path('finish_order/<int:pk>/', finish_order, name='finish_order'),

]