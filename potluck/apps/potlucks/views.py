from django.views.generic import ListView, DetailView, UpdateView

from .models import Order, CustomerOrder

from goods.views import ProductFilterFields, Ratings
from goods.models import Category, Rating


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
                                                       review__product__id=self.object.product.id).count()

        context['avg_rating'] = self.object.product.avg_rating
        context['stars'] = self.stars


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

