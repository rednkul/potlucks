from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import ProductToRetail, CategoryToRetail, OrderToRetail, OrderItem
from potlucks.models import Manufacturer
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .forms import OrderCreateForm

# Create your views here.
class ProductToRetailFilterFields:
    """Поля для фильтров"""

    def get_categories(self):
        """Категории"""
        return CategoryToRetail.objects.all()

class CategoryProductFilterFields:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.product_list = []


    def get_manufacturers(self, product_list):
        manufacturers = Manufacturer.objects.filter(manufacturer_products_retail__in=product_list).distinct()

        return manufacturers



class ProductsToRetailView(ProductToRetailFilterFields, ListView):
    queryset = ProductToRetail.objects.all()
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'retail/products/products_view.html'
    context_object_name = 'product_list'


class FilterProductsView(ProductToRetailFilterFields, ListView):
    """Фильтрация продуктов по категории/поставщику/производителю"""
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'retail/products/products_view.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        get_categories = self.request.GET.getlist("category")

        categories = CategoryToRetail.objects.filter(id__in=[int(i) for i in get_categories])
        subcategories = CategoryToRetail.objects.none()

        for category in categories:
            subcategories = subcategories | category.get_descendants()
        categories = (categories | subcategories).distinct()

        print(categories)
        category_filter = categories if categories else self.get_categories()

        queryset = ProductToRetail.objects.filter(category__in=category_filter)

        return queryset

    def get_context_data(self, *args, **kwargs):
        get_categories = self.request.GET.getlist("category")

        context = super().get_context_data(*args, **kwargs)
        context['categories'] = [int(i) for i in get_categories]

        context['category'] = ''.join([f"category={x}&" for x in get_categories])

        return context

class ProductToRetailDetailView(DetailView):
    model = ProductToRetail
    slug_field = 'url'
    context_object_name = 'product'
    template_name = 'retail/products/product_detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #ratings = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5}

        # for verb, value in ratings.items():
        #     context[f'{verb}'] = Rating.objects.filter(star__value=value,
        #                                                customer_order__order__product=self.object).count()

        #context['avg_rating'] = self.object.avg_rating
        #context['stars'] = self.stars
        context['categories'] = self.object.category.get_ancestors(include_self=True)
        context['form'] = CartAddProductForm()
        return context


class CategoryToRetailListView(ListView):
    queryset = CategoryToRetail.objects.all().order_by('id')
    context_object_name = 'categories'
    template_name = 'retail/categories/categories.html'

class CategoryToRetailDetailView(CategoryProductFilterFields, DetailView):
    model = CategoryToRetail
    slug_field = 'url'
    template_name = 'retail/categories/category_detail.html'
    context_object_name = 'category'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        category_list = self.object.get_descendants(include_self=True)

        products = ProductToRetail.objects.filter(category__in=category_list)


        context['product_list'] = products
        context['manufacturers'] = self.get_manufacturers(products)


        return self.render_to_response(context)

class CategoryProductsToRetailFilterView(CategoryProductFilterFields, ListView):
    paginate_by = 15
    paginate_orphans = 3
    template_name = 'retail/categories/category_detail.html'

    def get_category(self):
        url = self.request.path
        third_slash = url.find('/', 3)
        fourth_slash = url.rfind('/', 1)

        category_url = url[third_slash + 1:fourth_slash]

        category = CategoryToRetail.objects.get(url=category_url)

        return category

    def get_queryset(self):
        get_manufacturers = self.request.GET.getlist("manufacturer")

        # Получаю категорию по ее url
        category = self.get_category()

        # Получаю список, состоящий из категории и ее подкатегорий
        category_list = category.get_descendants(include_self=True)

        # Создаю список всех продуктов категории и подкатегорий
        self.product_list = ProductToRetail.objects.filter(category__in=category_list)

        manufacturers_filter = get_manufacturers if get_manufacturers else self.get_manufacturers(self.product_list)

        # Получаю продукты, принадлежащиии  к полученным категория и отвечающим условию фильтрации
        product_list = ProductToRetail.objects.filter(category__in=category_list, manufacturer__in=manufacturers_filter)
        return product_list


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )

            # очистка корзины
            cart.clear()
            return render(request, 'retail/orders/order_created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'retail/orders/order_create.html',
                  {'cart': cart, 'form': form})



