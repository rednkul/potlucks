from django.urls import path


from . import views
from . import services
app_name = 'potlucks'

urlpatterns = [

    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order_filter/', views.OrderFilterView.as_view(), name='order_filter'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/join/', services.join_an_order, name='join_an_order'),
    path('update_customer_order/<int:pk>/', services.update_customer_order, name='update_customer_order'),
    path('cancel_customer_order/<int:pk>/', services.cancel_customer_order, name='cancel_customer_order'),
    path('customer_order_checkout/<int:pk>/', views.CustomerOrderCheckoutView.as_view(), name='customer_order_checkout'),



]
