from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Order, Category, Product, Vendor, Manufacturer


class FilterFields:
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



class CategoriesView(ListView):
    queryset = Category.objects.filter(parent=None,).order_by('id')[:3]
    paginate_by = 3
    paginate_orphans = 1
    template_name = 'potlucks/home_page.html'


class ProductsView(FilterFields, ListView):
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
    template_name = 'potlucks/categories.html'


class CategoryDetailView(DetailView):
    model = Category
    slug_field = 'url'


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
        self.category_list.append(category)
        context['category_list'] = self.get_subcategories(category)
        context['category'] = category
        return self.render_to_response(context)



class FilterProductsView(FilterFields, ListView):
    """Фильтрация фильмов по году/жанру"""
    # paginate_by = 3
    # paginate_orphans = 1

    def get_queryset(self):
        get_categories = self.request.GET.getlist("category")
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturer = self.request.GET.getlist("manufacturer")


        category_filter = get_categories if get_categories else self.get_categories()
        vendors_filter = get_vendors if get_vendors else self.get_vendors()
        manufacturer_filter = get_manufacturer if get_manufacturer else self.get_manufacturers()



        queryset = Product.objects.filter(category__in=category_filter,
                                          vendors__in=vendors_filter,
                                          manufacturer_in=manufacturer_filter,
        )
        # elif get_vendors and not get_categories and not get_manufacturer:
        #     queryset = Product.objects.filter(vendors__in=get_vendors)
        #
        # elif get_manufacturer and not get_vendors and not get_categories:
        #     queryset = Product.objects.filter(manufacturer__in=get_manufacturer)
        #
        # elif get_categories and get_vendors and not get_manufacturer:
        #     queryset = Product.objects.filter(category__in=get_categories, vendors__in=get_vendors)
        # else:
        #     queryset = Movie.objects.filter(year__in=get_years, genres__in=get_genres, draft=False)
        #
        # return queryset

    def get_context_data(self, *args, **kwargs):
        get_categories = self.request.GET.getlist("category")
        get_vendors = self.request.GET.getlist("vendor")
        get_manufacturer = self.request.GET.getlist("manufacturer")

        context = super().get_context_data(*args, **kwargs)
        context['category'] = ''.join([f"category={x}&" for x in get_categories])
        context['vendor'] = ''.join([f"vendor={x}&" for x in get_vendors])
        context['manufacturer'] = ''.join([f"manufacturer={x}&" for x in get_manufacturer])
        return context
