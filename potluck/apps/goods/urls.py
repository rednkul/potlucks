from django.urls import path


from . import views
from . import services

app_name = 'goods'


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('search/', views.Search.as_view(), name='search'),

    # Категории
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/new_category/', views.CategoryCreateView.as_view(), name='new_category'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category_filter/<slug:slug>/', views.CategoryDetailFilterView.as_view(), name='category_filter'),

    # Товары
    path('products/', views.ProductsView.as_view(), name='products'),
    path('products/new_product/', views.ProductCreateView.as_view(), name='new_product'),
    path('products/edit_product/<slug:slug>/', views.ProductEditView.as_view(), name='edit_product'),
    path('products_filter/', views.FilterProductsView.as_view(), name='products_filter'),
    # path('json_products_filter/', views.JsonProductFilter.as_view(), name='json_products_filter'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Вишлист
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    # Отзывы
    path('review_and_rate/<int:pk>/', services.review_and_rate, name='review_and_rate'),

    # Производители
    path('manufacturers/new_manufacturer/', views.ManufacturerCreateView.as_view(), name='new_manufacturer'),
    path('manufacturers/edit_manufacturer/<int:pk>/', views.ManufacturerEditView.as_view(), name='edit_manufacturer'),
    path('manufacturers/<slug:slug>/', views.ManufacturerDetailView.as_view(), name='manufacturer_detail'),



]
