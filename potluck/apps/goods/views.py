from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.http import JsonResponse, HttpResponse, HttpResponseServerError

from .models import Product, Category, Manufacturer, RatingStar, Rating, Wishlist, Review
from .utils import get_subcategories_of_categories

from .templatetags.product_tag import get_most_popular_products
from cart.forms import CartAddProductForm
from retail.models import OrderItem
from potlucks.models import Potluck, Part
from users.mixins import GroupRequiredMixin


class Ratings:

    @property
    def stars(self):
        return RatingStar.objects.all()

    @classmethod
    def number_of_ratings(self):
        ratings = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5}
        return ratings


class HomePageView(Ratings, ListView):
    queryset = Category.objects.filter(parent=None, ).order_by('id')[:3]

    template_name = 'goods/home_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['new_products'] = Product.objects.order_by('id')[:5]
        context['most_popular_products'] = get_most_popular_products()['most_popular_products']

        context['stars'] = self.stars
        return context


class CategoryProductFilterFields:

    def get_manufacturers(self, product_list):
        manufacturers = Manufacturer.objects.filter(manufacturer_products__in=product_list).distinct()

        return manufacturers


class SearchPage:

    def define_search_page(self):

        search_option = self.request.GET['search_option']

        if int(search_option):
            return 'potlucks/potlucks/potlucks_list.html'
        else:
            return 'goods/products_view/products_view.html'


class ProductFilterFields:
    """Поля для фильтров"""

    def get_categories(self):
        return Category.objects.all()

    def get_manufacturers(self):
        return Manufacturer.objects.all()

    def get_max_price(self):
        return Product.objects.aggregate(Max('price'))['price__max']

    def get_min_price(self):
        return Product.objects.aggregate(Min('price'))['price__min']


class ProductsView(ProductFilterFields, ListView):
    queryset = Product.objects.all()
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'goods/products_view/products_view.html'

    def get_queryset(self):
        return Product.objects.all() if self.request.user.is_staff else Product.objects.filter(available=True)
    def get_context_data(self):
        context = super().get_context_data()
        context['min_price'] = self.get_min_price()
        context['max_price'] = self.get_max_price()
        return context

class FilterProductsView(ProductFilterFields, ListView):
    """Фильтрация продуктов по категории/поставщику/производителю"""
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'goods/products_view/products_view.html'

    def get_queryset(self):
        get_categories = self.request.GET.getlist("category")
        get_manufacturers = self.request.GET.getlist("manufacturer")
        get_available = self.request.GET.getlist("available")
        min_price = self.request.GET.get('price-min')
        max_price = self.request.GET.get('price-max')

        categories = get_subcategories_of_categories(get_categories)
        category_filter = categories if categories else self.get_categories()
        manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers()

        if self.request.user.is_staff and get_available:
            availability_filter = get_available
        elif self.request.user.is_staff:
            availability_filter = (True, False)
        else:
            availability_filter = (True,)


        queryset = Product.objects.filter(category__in=category_filter,
                                          manufacturer__in=manufacturers_filter,
                                          available__in=availability_filter,
                                          price__range=(min_price, max_price)
                                          ).distinct()
        print(queryset)

        return queryset

    def get_context_data(self, *args, **kwargs):
        get_categories = self.request.GET.getlist("category")
        get_manufacturers = self.request.GET.getlist("manufacturer")
        get_available = self.request.GET.getlist("available")
        min_price = self.request.GET.get('price-min')
        max_price = self.request.GET.get('price-max')

        context = super().get_context_data(*args, **kwargs)

        context['categories'] = [int(i) for i in get_categories]
        context['manufacturers'] = [int(i) for i in get_manufacturers]
        context['available'] = get_available
        context['min_price'] = min_price
        context['max_price'] = max_price


        return context


class ProductDetailView(Ratings, DetailView):
    model = Product
    slug_field = 'url'
    template_name = 'goods/products_view/product_detail.html'

    @property
    def is_ordered_by_user(self):
        if self.request.user.is_authenticated:
            return OrderItem.objects.filter(order__customer=self.request.user.profile.id,
                                            product=self.object.id).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for verb, value in Ratings.number_of_ratings().items():
            context[f'{verb}'] = Rating.objects.filter(star__value=value,
                                                       review__product=self.object).count()

        context['avg_rating'] = self.object.avg_rating
        context['stars'] = self.stars
        context['parts'] = Part.objects.filter(send=True, potluck__product=self.object)
        context['categories'] = self.object.category.get_ancestors(include_self=True)
        context['cart_product_form'] = CartAddProductForm()
        context['is_ordered'] = self.is_ordered_by_user

        return context


class CategoryListView(ListView):
    queryset = Category.objects.all().order_by('id')
    context_object_name = 'categories'
    template_name = 'goods/categories/categories.html'


class CategoryDetailView(CategoryProductFilterFields, DetailView):
    model = Category
    slug_field = 'url'
    template_name = 'goods/categories/category_detail.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        category_list = self.object.get_descendants(include_self=True)

        products = Product.objects.filter(category__in=category_list)

        context['category'] = self.object
        context['product_list'] = products
        context['manufacturers'] = self.get_manufacturers(products)

        return self.render_to_response(context)


class CategoryDetailFilterView(CategoryProductFilterFields, DetailView):
    paginate_by = 15
    model = Category
    slug_field = 'url'
    paginate_orphans = 3
    template_name = 'goods/categories/category_detail.html'

    def get_context_data(self, **kwargs):
        get_manufacturers = self.request.GET.getlist("manufacturer")
        category = self.object

        category_list = category.get_descendants(include_self=True)

        product_list = Product.objects.filter(category__in=category_list)

        # Условием фильтрации задаю отмеченные в форме пункты либо при их отсутствии - списки
        # производителей, связанных с полученным списком продуктов

        manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers(product_list)

        # Получаю продукты, принадлежащиии  к полученным категория и отвечающим условию фильтрации
        product_list = Product.objects.filter(category__in=category_list,
                                              manufacturer__in=manufacturers_filter)
        context = super().get_context_data(**kwargs)
        context['category_list'] = category_list
        context['product_list'] = product_list
        context['category'] = category
        context['manufacturers'] = manufacturers_filter

        context['manufacturer'] = ''.join([f"manufacturer={x}&" for x in get_manufacturers])
        return context


# class CategoryProductsFilterView(CategoryProductFilterFields, ListView):
#     paginate_by = 15
#     paginate_orphans = 3
#     template_name = 'goods/categories/category_detail.html'
#
#     def get_category(self):
#         url = self.request.path
#         first_slash = url.find('/', 1)
#         second_slash = url.rfind('/', 1)
#
#         category_url = url[first_slash + 1:second_slash]
#
#         category = Category.objects.get(url=category_url)
#
#         return category
#
#     def get_queryset(self):
#         get_manufacturers = self.request.GET.getlist("manufacturer")
#
#         # Получаю категорию по ее url
#         category = self.get_category()
#
#         # Получаю список, состоящий из категории и ее подкатегорий
#         category_list = category.get_descendants(include_self=True)
#
#         # Создаю список всех продуктов категории и подкатегорий
#         self.product_list = Product.objects.filter(category__in=category_list)
#
#         # Условием фильтрации задаю отмеченные в форме пункты либо при их отсутствии - списки
#         #  производителей, связанных с полученным списком продуктов
#         manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers(self.product_list)
#
#         # Получаю продукты, принадлежащиии  к полученным категория и отвечающим условию фильтрации
#         product_list = Product.objects.filter(category__in=category_list,
#                                               manufacturer__in=manufacturers_filter)
#         return product_list
#
#     def get_context_data(self, *args, **kwargs):
#         get_manufacturer = self.request.GET.getlist("manufacturer")
#
#         category = self.get_category()
#
#         context = super().get_context_data(*args, **kwargs)
#         print(context)
#
#         manufacturers = self.get_manufacturers(self.product_list)
#
#         context['category'] = category
#         context['manufacturers'] = manufacturers

#         context['manufacturer'] = ''.join([f"manufacturer={x}&" for x in get_manufacturer])
#         return context





class Search(ProductFilterFields, ListView):
    """Поиск по названию"""
    paginate_by = 15
    paginate_orphans = 3

    # paginate_orphans = 3

    def get_template_names(self):
        return self.define_search_page()

    def define_search_page(self):

        search_option = self.request.GET.get('search_option')

        if search_option == 'potlucks':
            return 'potlucks/potlucks/potlucks_list.html'
        else:
            return 'goods/products_view/products_view.html'

    def get_queryset(self):

        request = self.request.GET.get('q')
        option = self.request.GET.get('search_option')

        categories = Category.objects.filter(name__iregex=request)

        subcategories = Category.objects.none()

        for category in categories:
            subcategories = subcategories | category.get_descendants()

        categories = (categories | subcategories).distinct()

        if option == 'potlucks':
            return Potluck.objects.filter(Q(product__name__iregex=request) |
                                          Q(product__category__in=categories) |
                                          Q(product__description__iregex=request) |
                                          Q(product__tags__iregex=request)
                                          )

        else:
            return Product.objects.filter(Q(name__iregex=request) |
                                          Q(category__in=categories) |
                                          Q(description__iregex=request) |
                                          Q(tags__iregex=request)
                                          )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        option = self.request.GET.get('search_option')
        context['search_option'] = option
        print(context['search_option'])
        context['search'] = self.request.GET.get('q')
        context['q'] = f"q={self.request.GET.get('q')}&"

        return context


class WishlistView(DetailView):
    model = Wishlist
    template_name = 'goods/wishlist.html'

    def get_object(self):
        return Wishlist.objects.get(customer=self.request.user.profile.id)


class ProductCreateView(GroupRequiredMixin, CreateView):
    group_required = ['Manager', ]
    model = Product
    template_name = 'goods/products_view/new_product.html'
    # form_class = AddProductForm
    fields = ['name', 'category', 'manufacturer', 'description', 'tags', 'url', 'available', 'stock', 'price', 'image']
    success_url = reverse_lazy('goods:products')


class ProductEditView(GroupRequiredMixin, UpdateView):
    group_required = ['Manager', ]
    model = Product
    slug_field = 'url'
    template_name = 'goods/products_view/edit_product.html'
    fields = ['name', 'category', 'manufacturer', 'description', 'tags', 'url', 'available', 'stock', 'price', 'image']
    success_url = reverse_lazy('goods:products')


class CategoryCreateView(GroupRequiredMixin, CreateView):
    group_required = ['Manager', ]
    model = Category
    template_name = 'goods/categories/new_category.html'
    # form_class = AddProductForm
    fields = ['name', 'description', 'image', 'url', 'parent']
    success_url = reverse_lazy('goods:categories')


class ManufacturerCreateView(GroupRequiredMixin, CreateView):
    group_required = ['Manager', ]
    model = Manufacturer
    template_name = 'goods/manufacturers/new_manufacturer.html'
    fields = ['name', 'description', 'image', 'url']
    success_url = reverse_lazy('goods:products')


class ManufacturerDetailView(GroupRequiredMixin, DetailView):
    group_required = ['Manager', ]
    model = Manufacturer
    slug_field = 'url'
    template_name = 'goods/manufacturers/manufacturer_detail.html'


class ManufacturerEditView(GroupRequiredMixin, UpdateView):
    group_required = ['Manager', ]
    model = Manufacturer
    slug_field = 'url'
    template_name = 'goods/manufacturers/edit_manufacturer.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('goods:manufacturer_detail', self.object.id)
