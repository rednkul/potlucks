from django.urls import path, include


from .views import CategoriesView, ProductsView, ProductDetailView, CategoryListView, CategoryDetailView, \
    FilterProductsView, CategoryProductsFilterView

app_name = 'potlucks'

urlpatterns = [
    path('', CategoriesView.as_view(), name='home_page'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category_filter/<slug:slug>/', CategoryProductsFilterView.as_view(), name='category_filter'),
    path('products/', ProductsView.as_view(), name='products'),
    path('products_filter/', FilterProductsView.as_view(), name='product_filter'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
