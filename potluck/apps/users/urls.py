from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile_detail/', login_required(views.ProfileDetailView.as_view()), name='profile_detail'),
    path('my_orders/', login_required(views.UserOrdersListView.as_view()), name='user_orders'),
    path('my_parts/', login_required(views.UserPartsListView.as_view()), name='user_parts'),
    path('my_part_orders/', login_required(views.UserPartOrdersListView.as_view()), name='user_part_orders'),

]