from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile_detail/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('change_password/', views.change_password, name='change_password'),
    path('my_orders/', views.UserOrdersListView.as_view(), name='user_orders'),
    path('my_parts/', views.UserPartsListView.as_view(), name='user_parts'),
    path('my_part_orders/', views.UserPartOrdersListView.as_view(), name='user_part_orders'),

]