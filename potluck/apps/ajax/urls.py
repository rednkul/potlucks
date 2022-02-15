from django.urls import path
from . import views

app_name = 'ajax'

urlpatterns = [
    path('validate_goods_number/<int:pk>/', views.validate_goods_number, name='validate_goods_number'),
    path('validate_email/', views.validate_email, name='validate_email'),
    path('validate_email_to_reset_password/', views.validate_email_to_reset_password,
         name='validate_email_to_reset_password'),
    path('add_product_to_wishlist/<int:pk>', views.add_product_to_wishlist, name='add_product_to_wishlist'),
    path('delete_product_from_wishlist/<int:pk>', views.delete_product_from_wishlist, name='delete_product_from_wishlist'),
]
