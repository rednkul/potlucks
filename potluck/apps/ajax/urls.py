from django.urls import path
from . import views
from . import services
app_name = 'ajax'

urlpatterns = [
    path('validate_goods_number/<int:pk>/', views.validate_goods_number, name='validate_goods_number'),
    path('validate_email/', views.validate_email, name='validate_email'),
    path('validate_email_to_reset_password/', views.validate_email_to_reset_password,
         name='validate_email_to_reset_password'),
    path('add_product_to_wishlist/<int:pk>/', views.add_product_to_wishlist, name='add_product_to_wishlist'),
    path('delete_product_from_wishlist/<int:pk>/', views.delete_product_from_wishlist, name='delete_product_from_wishlist'),
    path('product_make_available/<int:pk>/', views.product_make_available, name='product_make_available'),
    path('product_make_unavailable/<int:pk>/', views.product_make_unavailable, name='product_make_unavailable'),
    path('order_confirm/<str:order_type>/<int:pk>/', services.confirm_order, name='confirm_order'),
    path('order_disconfirm/<str:order_type>/<int:pk>/', services.disconfirm_order, name='disconfirm_order'),
    path('order_paid/<str:order_type>/<int:pk>/', services.paid_order, name='paid_order'),
    path('order_unpaid/<str:order_type>/<int:pk>/', services.unpaid_order, name='unpaid_order'),
    path('order_delete/<str:order_type>/<int:pk>/', services.unpaid_order, name='delete_order'),

]
