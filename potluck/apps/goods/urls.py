from django.urls import path


from . import views
from . import services

app_name = 'goods'


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('search/', views.Search.as_view(), name='search'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category_filter/<slug:slug>/', views.CategoryProductsFilterView.as_view(), name='category_filter'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('products_filter/', views.FilterProductsView.as_view(), name='products_filter'),
    # path('json_products_filter/', views.JsonProductFilter.as_view(), name='json_products_filter'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/<int:pk>/', views.WishlistView.as_view(), name='wishlist'),
    path('review_and_rate/<int:pk>/', services.review_and_rate, name='review_and_rate'),
]
