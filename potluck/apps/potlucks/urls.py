from django.urls import path


from . import views
from . import services
app_name = 'potlucks'

urlpatterns = [

    path('', views.PotluckListView.as_view(), name='potlucks'),
    path('potluck_filter/', views.PotluckFilterView.as_view(), name='potluck_filter'),
    path('<int:pk>/', views.PotluckDetailView.as_view(), name='potluck_detail'),
    path('<int:pk>/join/', services.join_potluck, name='join_potluck'),
    path('update_part/<int:pk>/', services.update_part, name='update_part'),
    path('cancel_part/<int:pk>/', services.cancel_part, name='cancel_part'),
    path('part_checkout/<int:part_pk>/', views.part_order_create, name='part_checkout'),
    path('part_order_created/<int:part_order_id>/', views.part_order_created, name='part_order_created'),
    path('new_potluck/', views.PotluckCreateView.as_view(), name='new_potluck'),
    path('edit_potluck/<int:pk>', views.PotluckEditView.as_view(), name='edit_potluck'),

    # Поставщики
    path('vendors/new_vendor/', views.VendorCreateView.as_view(), name='new_vendor'),
    path('vendors/edit_vendor/<int:pk>/', views.VendorEditView.as_view(), name='edit_vendor'),
    path('vendors/<slug:slug>/', views.VendorDetailView.as_view(), name='vendor_detail'),
    path('part_orders/', views.PartOrderListView.as_view(), name='part_orders'),
    path('part_orders/json_filter', views.JsonPartOrderFilterListView.as_view(), name='json_part_orders_filter'),
]
