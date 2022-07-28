from django.urls import path


from . import views
from . import services
app_name = 'potlucks'

urlpatterns = [

    path('', views.PotluckListView.as_view(), name='potlucks'),
    path('potluck_filter/', views.PotluckFilterView.as_view(), name='potluck_filter'),
    path('potlucks/<int:pk>/', views.PotluckDetailView.as_view(), name='potluck_detail'),
    path('potlucks/<int:pk>/join/', services.join_potluck, name='join_potluck'),
    path('update_part/<int:pk>/', services.update_part, name='update_part'),
    path('cancel_part/<int:pk>/', services.cancel_part, name='cancel_part'),
    path('part_checkout/<int:part_pk>/', views.part_order_create, name='part_checkout'),
    path('part_order_created/<int:part_order_id>/', views.part_order_created, name='part_order_created'),

]
