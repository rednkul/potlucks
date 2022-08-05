from django.db.models import Q, Count, Sum, Avg
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.http import JsonResponse

from potlucks.models import Potluck, Part


from .models import Product, Category, Manufacturer, RatingStar, Rating, Wishlist, Review
from .utils import get_subcategories_of_categories

from cart.forms import CartAddProductForm
from retail.models import OrderItem

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
        context['most_popular_products'] = sorted(Product.objects.all(), key=lambda x: x.potlucks.count(),
                                                  reverse=True)[:5]

        context['stars'] = self.stars
        return context

class CategoryProductFilterFields:


    # def get_vendors(self, product_list):
    #
    #     vendors = Vendor.objects.filter(vendor_products__in=product_list).distinct()
    #
    #     return vendors

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
        """Категории"""
        return Category.objects.all()


    def get_manufacturers(self):
        """"Производители"""
        return Manufacturer.objects.all()

    # def get_years(self):
    #     #print(sorted(Movie.objects.filter(draft=False).values_list("year", flat=True).distinct()))
    #     return sorted(Movie.objects.filter(draft=False).values_list("year", flat=True).distinct())






class ProductsView(ProductFilterFields, ListView):
    queryset = Product.objects.all()
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'goods/products_view/products_view.html'


class ProductDetailView(Ratings, DetailView):
    model = Product
    slug_field = 'url'
    template_name = 'goods/products_view/product_detail.html'

    @property
    def is_ordered_by_user(self):
        if self.request.user.is_authenticated:
            return OrderItem.objects.filter(order__customer=self.request.user.profile.id, product=self.object.id).exists()


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


class FilterProductsView(ProductFilterFields, ListView):
    """Фильтрация продуктов по категории/поставщику/производителю"""
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'goods/products_view/products_view.html'

    def get_queryset(self):
        get_categories = self.request.GET.getlist("category")
        get_manufacturers = self.request.GET.getlist("manufacturer")



        categories = get_subcategories_of_categories(get_categories)



        print(f'-----------------------{categories}------------------')
        category_filter = categories if categories else self.get_categories()
        manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers()

        queryset = Product.objects.filter(category__in=category_filter,
                                          manufacturer__in=manufacturers_filter,
                                          ).distinct()

        return queryset

    def get_context_data(self, *args, **kwargs):
        get_categories = self.request.GET.getlist("category")
        get_manufacturer = self.request.GET.getlist("manufacturer")

        context = super().get_context_data(*args, **kwargs)

        context['categories'] = [int(i) for i in get_categories]
        context['manufacturers'] = [int(i) for i in get_manufacturer]

        context['category'] = ''.join([f"category={x}&" for x in get_categories])
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


class ProductCreateView(CreateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Product
    template_name = 'goods/products_view/new_product.html'
    #form_class = AddProductForm
    fields = [ 'name', 'category', 'manufacturer', 'description', 'tags', 'url', 'available', 'stock', 'price', 'image']
    success_url = reverse_lazy('goods:products')

class ProductEditView(UpdateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Product
    slug_field = 'url'
    template_name = 'goods/products_view/edit_product.html'
    fields = [ 'name', 'category', 'manufacturer', 'description', 'tags', 'url', 'available', 'stock', 'price', 'image']
    success_url = reverse_lazy('goods:products')

class CategoryCreateView(CreateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Category
    template_name = 'goods/categories/new_category.html'
    #form_class = AddProductForm
    fields = [ 'name', 'description', 'image', 'url', 'parent']
    success_url = reverse_lazy('goods:categories')

class ManufacturerCreateView(CreateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Manufacturer
    template_name = 'goods/manufacturers/new_manufacturer.html'
    fields = [ 'name', 'description', 'image', 'url']
    success_url = reverse_lazy('goods:products')

class ManufacturerDetailView(DetailView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Manufacturer
    slug_field = 'url'
    template_name = 'goods/manufacturers/manufacturer_detail.html'

class ManufacturerEditView(UpdateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Manufacturer
    slug_field = 'url'
    template_name = 'goods/manufacturers/edit_manufacturer.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('goods:manufacturer_detail', self.object.id)




