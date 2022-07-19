from django.urls import path

from . import views

app_name = 'retail'

urlpatterns = [
    path('products', views.ProductsToRetailView.as_view(), name='products'),
    path('products_filter/', views.FilterProductsView.as_view(), name='products_filter'),
    path('products/<slug:slug>/', views.ProductToRetailDetailView.as_view(), name='product_detail'),
    path('categories/', views.CategoryToRetailListView.as_view(), name='categories'),
    path('categories/<slug:slug>/', views.CategoryToRetailDetailView.as_view(), name='category_detail'),
    path('category_filter/<slug:slug>/', views.CategoryProductsToRetailFilterView.as_view(), name='category_filter'),
    path('order_create/', views.order_create, name='order_create'),

]