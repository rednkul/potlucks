from django.urls import path

from .services import join_an_order
from .views import CategoriesView, ProductsView, ProductDetailView, CategoryListView, CategoryDetailView, \
    FilterProductsView, CategoryProductsFilterView, Search, OrderListView, OrderFilterView, OrderDetailView


app_name = 'potlucks'

urlpatterns = [
    path('', CategoriesView.as_view(), name='home_page'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order_filter/', OrderFilterView.as_view(), name='order_filter'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/join/', join_an_order, name='join_an_order'),
    path('search/', Search.as_view(), name='search'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category_filter/<slug:slug>/', CategoryProductsFilterView.as_view(), name='category_filter'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products_filter/', FilterProductsView.as_view(), name='product_filter'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),


]
