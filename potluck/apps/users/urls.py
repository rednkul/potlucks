from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('change_password/', views.change_password, name='change_password')

]