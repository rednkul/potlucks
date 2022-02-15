from django.urls import path

from .services import join_an_order
from . import views
from . import services
app_name = 'potlucks'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order_filter/', views.OrderFilterView.as_view(), name='order_filter'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/join/', services.join_an_order, name='join_an_order'),
    path('search/', views.Search.as_view(), name='search'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category_filter/<slug:slug>/', views.CategoryProductsFilterView.as_view(), name='category_filter'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('products_filter/', views.FilterProductsView.as_view(), name='products_filter'),
    #path('json_products_filter/', views.JsonProductFilter.as_view(), name='json_products_filter'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('update_customer_order/<int:pk>/', services.update_customer_order, name='update_customer_order'),
    path('cancel_customer_order/<int:pk>/', services.cancel_customer_order, name='cancel_customer_order'),
    path('customer_order_checkout/<int:pk>/', views.CustomerOrderCheckoutView.as_view(), name='customer_order_checkout'),
    path('review_and_rate/<int:pk>', services.review_and_rate, name='review_and_rate'),
    path('wishlist/<int:pk>/', views.WishlistView.as_view(), name='wishlist'),

]
