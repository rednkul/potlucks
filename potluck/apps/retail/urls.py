from django.urls import path

from . import views

app_name = 'retail'

urlpatterns = [
    path('order_create/', views.order_create, name='order_create'),
    path('order_created/<int:order_id>/', views.order_created, name='order_created'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/filter', views.OrderFilterListView.as_view(), name='orders_filter'),
    path('orders/json_filter', views.JsonOrderFilterListView.as_view(), name='json_orders_filter'),

]