import json

from django.db.models import Q, Count, Sum, Avg
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.http import JsonResponse
# from django_braintree.forms import TransactionForm

import time

from .models import Order, Category, Product, Vendor, Manufacturer, CustomerOrder, RatingStar, Rating, Wishlist
from .services import join_an_order


class Ratings:

    @property
    def stars(self):
        return RatingStar.objects.all()

class SearchPage:

    def define_search_page(self):

        search_option = self.request.GET['search_option']

        if int(search_option):
            return 'potlucks/orders/orders.html'
        else:
            return 'potlucks/products_view/products_view.html'


class ProductFilterFields:
    """Поля для фильтров"""

    def get_categories(self):
        """Категории"""
        return Category.objects.all()

    def get_vendors(self):
        """"Поставщики"""
        return Vendor.objects.all()

    def get_manufacturers(self):
        """"Производители"""
        return Manufacturer.objects.all()

    # def get_years(self):
    #     #print(sorted(Movie.objects.filter(draft=False).values_list("year", flat=True).distinct()))
    #     return sorted(Movie.objects.filter(draft=False).values_list("year", flat=True).distinct())


class CategoryProductFilterFields:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.product_list = []



    def get_vendors(self, product_list):

        vendors = Vendor.objects.filter(vendor_products__in=product_list).distinct()

        return vendors

    def get_manufacturers(self, product_list):
        manufacturers = Manufacturer.objects.filter(manufacturer_products__in=product_list).distinct()

        return manufacturers


class HomePageView(Ratings, ListView) :
    queryset = Category.objects.filter(parent=None, ).order_by('id')[:3]

    template_name = 'potlucks/home_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['new_products'] = Product.objects.order_by('id')[:5]
        context['most_popular_products'] = sorted(Product.objects.all(), key=lambda x: x.product_orders.count(),
                                                  reverse=True)[:5]

        context['stars'] = self.stars
        return context


class ProductsView(ProductFilterFields, ListView):
    queryset = Product.objects.all()
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'potlucks/products_view/products_view.html'


class ProductDetailView(Ratings,DetailView):
    model = Product
    slug_field = 'url'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ratings = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5}

        for verb, value in ratings.items():
            context[f'{verb}'] = Rating.objects.filter(star__value=value,
                                                       customer_order__order__product=self.object).count()

        context['avg_rating'] = self.object.avg_rating
        context['stars'] = self.stars
        context['customer_orders'] = CustomerOrder.objects.filter(send=True, order__product=self.object)
        context['categories'] = self.object.category.get_ancestors(include_self=True)

        return context


class CategoryListView(ListView):
    queryset = Category.objects.all().order_by('id')
    context_object_name = 'categories'
    template_name = 'potlucks/categories/categories.html'


class CategoryDetailView(CategoryProductFilterFields, DetailView):
    model = Category
    slug_field = 'url'
    template_name = 'potlucks/categories/category_detail.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        category_list = self.object.get_descendants(include_self=True)

        products = Product.objects.filter(category__in=category_list)

        context['category'] = self.object
        context['product_list'] = products
        context['manufacturers'] = self.get_manufacturers(products)

        return self.render_to_response(context)


class FilterProductsView(ProductFilterFields, ListView):
    """Фильтрация продуктов по категории/поставщику/производителю"""
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'potlucks/products_view/products_view.html'

    def get_queryset(self):
        get_categories = self.request.GET.getlist("category")
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturers = self.request.GET.getlist("manufacturer")



        categories = Category.objects.filter(id__in=[int(i) for i in get_categories])
        subcategories = Category.objects.none()

        for category in categories:
            subcategories = subcategories | category.get_descendants()

        categories = (categories | subcategories).distinct()



        print(f'-----------------------{categories}------------------')
        category_filter = categories if categories else self.get_categories()
        vendors_filter = get_vendors if get_vendors else self.get_vendors()
        manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers()

        queryset = Product.objects.filter(category__in=category_filter,
                                          vendors__in=vendors_filter,
                                          manufacturer__in=manufacturers_filter,
                                          )

        return queryset

    def get_context_data(self, *args, **kwargs):
        get_categories = self.request.GET.getlist("category")
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturer = self.request.GET.getlist("manufacturer")

        context = super().get_context_data(*args, **kwargs)
        context['categories'] = [int(i) for i in get_categories]
        context['vendors'] = [int(i) for i in get_vendors]
        context['manufacturers'] = [int(i) for i in get_manufacturer]

        context['category'] = ''.join([f"category={x}&" for x in get_categories])
        context['vendor'] = ''.join([f"vendor={x}&" for x in get_vendors])
        context['manufacturer'] = ''.join([f"manufacturer={x}&" for x in get_manufacturer])
        return context


class JsonProductFilter(ProductFilterFields, ListView):
    paginate_by = 15
    paginate_orphans = 3

    def get_queryset(self):
        get_categories = self.request.GET.getlist("category")
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturers = self.request.GET.getlist("manufacturer")

        print(f'cat-----------{get_categories}--------------')
        print(f'ven-----------{get_vendors}--------------')
        print(f'man-----------{get_manufacturers}--------------')
        # Создаю queryset категорий по их id, полученным из формы

        categories = Category.objects.filter(id__in=[int(i) for i in get_categories])
        subcategories = Category.objects.none()

        # Получаю потомков каждой из категорий и свожу их в один qs
        for category in categories:
            subcategories = subcategories | category.get_descendants()

        # Свожу qs подкатегорий и категорий
        categories = (categories | subcategories).distinct()

        category_filter = categories if categories else self.get_categories()
        vendors_filter = get_vendors if get_vendors else self.get_vendors()
        manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers()

        queryset = Product.objects.filter(category__in=category_filter,
                                          vendors__in=vendors_filter,
                                          manufacturer__in=manufacturers_filter,
                                          ).distinct().values(
            "name", "image"
        )

        return queryset

    def get(self, request, *arg, **kwargs):

        queryset = list(self.get_queryset())
        print(f'JSONчек-------------------{queryset}----------------------')
        return JsonResponse({"product_list": queryset}, safe=False)


class CategoryProductsFilterView(CategoryProductFilterFields, ListView):
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'potlucks/categories/category_detail.html'

    def get_category(self):
        url = self.request.path
        first_slash = url.find('/', 1)
        second_slash = url.rfind('/', 1)

        category_url = url[first_slash + 1:second_slash]

        category = Category.objects.get(url=category_url)

        return category

    def get_queryset(self):
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturers = self.request.GET.getlist("manufacturer")

        # Получаю категорию по ее url
        category = self.get_category()

        # Получаю список, состоящий из категории и ее подкатегорий
        category_list = category.get_descendants(include_self=True)

        # Создаю список всех продуктов категории и подкатегорий
        self.product_list = Product.objects.filter(category__in=category_list)

        # Условием фильтрации задаю отмеченные в форме пункты либо при их отсутствии - списки поставщиков
        # и производителей, связанных с полученным списком продуктов
        vendors_filter = get_vendors if get_vendors else self.get_vendors(self.product_list)
        manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers(self.product_list)

        # Получаю продукты, принадлежащиии  к полученным категория и отвечающим условию фильтрации
        product_list = Product.objects.filter(category__in=category_list, vendors__in=vendors_filter,
                                              manufacturer__in=manufacturers_filter)
        return product_list

    def get_context_data(self, *args, **kwargs):
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturer = self.request.GET.getlist("manufacturer")

        category = self.get_category()

        context = super().get_context_data(*args, **kwargs)

        vendors = self.get_vendors(self.product_list)
        manufacturers = self.get_manufacturers(self.product_list)

        context['category'] = category
        context['vendors'] = vendors
        context['manufacturers'] = manufacturers

        context['vendor'] = ''.join([f"vendor={x}&" for x in get_vendors])
        context['manufacturer'] = ''.join([f"manufacturer={x}&" for x in get_manufacturer])
        return context


class Search(ProductFilterFields, ListView):
    """Поиск по названию"""
    paginate_by = 15
    paginate_orphans = 3

    # paginate_orphans = 3

    def get_template_names(self):
        return self.define_search_page()

    def define_search_page(self):

        search_option = self.request.GET.get('search_option')

        if search_option == 'orders':
            return 'potlucks/orders/orders.html'
        else:
            return 'potlucks/products_view/products_view.html'

    def get_queryset(self):

        category_list = []
        request = self.request.GET.get('q')
        option = self.request.GET.get('search_option')

        categories = Category.objects.filter(name__iregex=request)

        subcategories = Category.objects.none()

        for category in categories:
            subcategories = subcategories | category.get_descendants()

        categories = (categories | subcategories).distinct()

        if option == 'orders':
            return Order.objects.filter(Q(product__name__iregex=request) |
                                        Q(product__category__in=category_list) |
                                        Q(product__description__iregex=request) |
                                        Q(product__tags__iregex=request)
                                        )

        else:
            return Product.objects.filter(Q(name__iregex=request) |
                                          Q(category__in=category_list) |
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


class OrderListView(ProductFilterFields, Ratings, ListView):
    queryset = Order.objects.filter(amassed=False)
    template_name = 'potlucks/orders/orders.html'
    paginate_by = 15
    paginate_orphans = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['stars'] = self.stars
        return context




class OrderFilterView(ProductFilterFields, ListView):
    template_name = 'potlucks/orders/orders.html'
    paginate_by = 15
    paginate_orphans = 3

    def get_queryset(self):
        get_categories = self.request.GET.getlist("category")
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturers = self.request.GET.getlist("manufacturer")

        # Создаю queryset категорий по их id, полученным из формы

        categories = Category.objects.filter(id__in=[int(i) for i in get_categories])
        subcategories = Category.objects.none()

        # Получаю потомков каждой из категорий и свожу их в один qs
        for category in categories:
            subcategories = subcategories | category.get_descendants()

        # Свожу qs подкатегорий и категорий
        categories = (categories | subcategories).distinct()

        category_filter = categories if categories else self.get_categories()
        vendors_filter = get_vendors if get_vendors else self.get_vendors()
        manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers()

        queryset = Order.objects.filter(product__category__in=category_filter,
                                        product__vendors__in=vendors_filter,
                                        product__manufacturer__in=manufacturers_filter,
                                        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        get_categories = self.request.GET.getlist("category")
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturer = self.request.GET.getlist("manufacturer")

        context = super().get_context_data(*args, **kwargs)
        context['category'] = ''.join([f"category={x}&" for x in get_categories])
        context['vendor'] = ''.join([f"vendor={x}&" for x in get_vendors])
        context['manufacturer'] = ''.join([f"manufacturer={x}&" for x in get_manufacturer])
        return context


class OrderDetailView(Ratings,DetailView):
    model = Order
    template_name = 'potlucks/orders/order_detail.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['available'] = self.object.size - self.object.get_order_fullness()
        context['categories'] = self.object.product.category.get_ancestors(include_self=True)
        context['is_partner'] = self.customer_ispartner()
        context['customer_order'] = self.get_customer_order() if self.customer_ispartner() else None

        ratings = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5}

        for verb, value in ratings.items():
            context[f'{verb}'] = Rating.objects.filter(star__value=value,
                                                       customer_order__order__product=self.object.product).count()

        context['avg_rating'] = self.object.product.avg_rating
        context['stars'] = self.stars
        context['customer_orders'] = CustomerOrder.objects.filter(send=True, order__product=self.object.product)

        return context

    def get_customer_order(self):
        order = self.get_object()
        customer_order = CustomerOrder.objects.get(order=order, customer=self.request.user.profile)
        print(f"corder---------------{customer_order.id}------")
        return customer_order

    def customer_ispartner(self):

        order = self.get_object()
        print(f"Партнер---------------{self.request.user.profile.id in order.partners}------")
        return self.request.user.profile.id in order.partners


class CustomerOrderCheckoutView(UpdateView):
    model = CustomerOrder
    template_name = 'potlucks/orders/customer_order_checkout.html'
    context_object_name = 'customer_order'
    fields = ['notes', ]


class CustomerOrderUpdateView(UpdateView):
    model = CustomerOrder
    template_name = 'potlucks/orders/customer_order_update.html'
    context_object_name = 'customer_order'
    fields = ['goods_number', ]

class WishlistView(DetailView):
    model = Wishlist
    template_name = 'potlucks/wishlist.html'