from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
import time

from .models import Order, Category, Product, Vendor, Manufacturer


class ProductFilterFields:
    """Поля для фильтров"""
    def get_categories(self):
        """Категории"""
        return Category.objects.all()

    def get_subcategories(self, obj, subcategory_list):
        if not obj.subcategories.all():
            return subcategory_list

        else:

            for subcategory in obj.subcategories.all():
                if subcategory not in subcategory_list:
                    subcategory_list.append(subcategory)
                return self.get_subcategories(subcategory, subcategory_list)

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
        self.category_list = []
        self.product_list = []

    def get_subcategories(self, obj):
        if not obj.subcategories.all():
            return self.category_list

        else:

            for subcategory in obj.subcategories.all():
                self.category_list.append(subcategory)
                return self.get_subcategories(subcategory)



    def get_vendors(self, product_list):

        vendors = Vendor.objects.filter(vendor_products__in=product_list).distinct()

        return vendors

    def get_manufacturers(self, product_list):
        manufacturers = Manufacturer.objects.filter(manufacturer_products__in=product_list).distinct()


        return manufacturers


class CategoriesView(ListView):
    queryset = Category.objects.filter(parent=None,).order_by('id')[:3]
    paginate_by = 3
    paginate_orphans = 1
    template_name = 'potlucks/home_page.html'


class ProductsView(ProductFilterFields, ListView):
    queryset = Product.objects.all()
    paginate_by = 20
    template_name = 'potlucks/products_view/products_view.html'

class ProductDetailView(DetailView):
    model = Product
    slug_field = 'url'

    def get_product_categories(self, obj):
        if obj.category:
            category = obj.category
            categories = [category.name, ]
            while category.parent:
                categories.append(category.parent.name)
                category = category.parent

            return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['categories'] = self.get_product_categories(self.object)
        return context


class CategoryListView(ListView):
    queryset = Category.objects.all().order_by('id')
    context_object_name = 'categories'
    template_name = 'potlucks/categories/categories.html'



class CategoryDetailView(CategoryProductFilterFields, DetailView):
    model = Category
    slug_field = 'url'
    template_name = 'potlucks/categories/category_detail.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_list = []


    def get_subcategories(self, obj):
        if not obj.subcategories.all():
            return self.category_list

        else:

            for subcategory in obj.subcategories.all():
                self.category_list.append(subcategory)
                return self.get_subcategories(subcategory)




    def get(self, request, slug, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(url=slug)

        category_list = [category, *self.get_subcategories(category)]




        products = Product.objects.filter(category__in=category_list)

        context['category'] = category
        context['product_list'] = products
        context['manufacturers'] = self.get_manufacturers(products)
        context['vendors'] = self.get_vendors(products)


        return self.render_to_response(context)


class FilterProductsView(ProductFilterFields, ListView):
    """Фильтрация продуктов по категории/поставщику/производителю"""
    # paginate_by = 3
    # paginate_orphans = 1
    template_name = 'potlucks/products_view/products_view.html'


    def get_queryset(self):
        get_categories = self.request.GET.getlist("category")
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturers = self.request.GET.getlist("manufacturer")

        # Создаю список категорий по их id, полученным из формы
        categories = []
        for id in get_categories:
            categories.append(Category.objects.get(id=int(id)))

        # Получаю список подкатегорий с присоединяю его к списку категорий
        if get_categories:
            subcategory_list = []
            for category in categories:
                subcategory_list = self.get_subcategories(category, subcategory_list)
            categories += subcategory_list

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
        context['category'] = ''.join([f"category={x}&" for x in get_categories])
        context['vendor'] = ''.join([f"vendor={x}&" for x in get_vendors])
        context['manufacturer'] = ''.join([f"manufacturer={x}&" for x in get_manufacturer])
        return context


class CategoryProductsFilterView(CategoryProductFilterFields, ListView):

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
        category_list = [category, *self.get_subcategories(category)]

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

    template_name = 'potlucks/products_view/products_view.html'
    def get_queryset(self):

        category_list = []
        request = self.request.GET.get('q')
        print(request)
        categories = Category.objects.filter(name__iregex=request)

        for category in categories:
            self.get_subcategories(category, category_list)

        for category in categories:
            if category not in category_list:
                category_list.append(category)

        return Product.objects.filter(Q(name__iregex=request) |
                                      Q(category__in=category_list) |
                                      Q(description__iregex=request))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"

        return context

