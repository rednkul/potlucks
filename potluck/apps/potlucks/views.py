from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from .models import Potluck, Part, PartOrder, Vendor

from goods.views import ProductFilterFields, Ratings
from goods.models import Category, Rating
from .forms import PartOrderCreateForm, PotluckCreateForm
from goods.utils import format_date


class PotluckFilterFields:
    def get_vendors(self):
        """"Поставщики"""
        print('ekekekekkeke')
        return Vendor.objects.all()

class PotluckListView(ProductFilterFields, PotluckFilterFields, Ratings, ListView):
    queryset = Potluck.objects.filter(amassed=False)
    template_name = 'potlucks/potlucks/potlucks_list.html'
    paginate_by = 15
    paginate_orphans = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['stars'] = self.stars
        return context


class PotluckFilterView(ProductFilterFields, PotluckFilterFields, ListView):
    template_name = 'potlucks/potlucks/potlucks_list.html'
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

        queryset = Potluck.objects.filter(product__category__in=category_filter,
                                          vendor__in=vendors_filter,
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


class PotluckDetailView(Ratings, DetailView):
    model = Potluck
    template_name = 'potlucks/potlucks/potluck_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['available'] = self.object.size - self.object.get_potluck_fullness()
        context['categories'] = self.object.product.category.get_ancestors(include_self=True)
        context['is_partner'] = self.customer_ispartner()
        context['part'] = self.get_part() if self.customer_ispartner() else None

        ratings = {'ones': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5}

        for verb, value in ratings.items():
            context[f'{verb}'] = Rating.objects.filter(star__value=value,
                                                       review__product__id=self.object.product.id).count()

        context['avg_rating'] = self.object.product.avg_rating
        context['stars'] = self.stars

        return context

    def get_part(self):
        potluck = self.get_object()
        part = Part.objects.get(potluck=potluck, customer=self.request.user.profile)
        return part

    def customer_ispartner(self):
        potluck = self.get_object()
        print(f"Партнер---------------{self.request.user.profile.id in potluck.partners}------")
        return self.request.user.profile.id in potluck.partners


def part_order_create(request, part_pk):
    part = Part.objects.get(id=part_pk)
    if request.method == 'POST':
        form = PartOrderCreateForm(request.POST)
        if form.is_valid():
            part_order = form.save()

            return redirect('potlucks:part_order_created', part_order_id=part_order.id)
    else:
        form = PartOrderCreateForm
    return render(request, 'potlucks/potlucks/part_checkout.html', {'form': form, 'part': part})

class PartOrderCreateView(CreateView):
    form_class = PartOrderCreateForm
    model = PartOrder
    template_name = 'potlucks/potlucks/part_checkout.html'


    def get_success_url(self):
        print('ЧО?')
        return reverse_lazy('potlucks:part_order_created', part_order_id=self.object.id)

    def get(self, request, part_pk, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        part = Part.objects.get(pk=part_pk)
        context['part'] = part
        return self.render_to_response(context)

def part_order_created(request, part_order_id):
    return render(request, 'potlucks/potlucks/part_order_created.html', {'part_order': part_order_id})

# class PartCheckoutView(UpdateView):
#     model = Part
#     template_name = 'potlucks/potlucks/part_checkout.html'
#     context_object_name = 'part'
#     fields = ['notes', ]


class PartUpdateView(UpdateView):
    model = Part
    template_name = 'potlucks/potlucks/part_update.html'
    context_object_name = 'part'
    fields = ['goods_number', ]

class PotluckCreateView(CreateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Potluck
    template_name = 'potlucks/potlucks/new_potluck.html'
    form_class = PotluckCreateForm
    success_url = reverse_lazy('potlucks:potlucks')

class PotluckEditView(UpdateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Potluck
    #slug_field = 'url'
    template_name = 'potlucks/potlucks/edit_potluck.html'
    fields = [ 'creator', 'vendor', 'unit_price']
    success_url = reverse_lazy('potlucks:potlucks')

class VendorCreateView(CreateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Vendor
    template_name = 'potlucks/vendors/new_vendor.html'
    fields = [ 'name', 'description', 'image', 'contact_phone', 'contact_site', 'contact_social', 'url']
    success_url = reverse_lazy('potlucks:potlucks')

class VendorEditView(UpdateView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Vendor
    template_name = 'potlucks/vendors/edit_vendor.html'
    fields = [ 'name', 'description', 'image', 'contact_phone', 'contact_site', 'contact_social', 'url']
    success_url = reverse_lazy('potlucks:potlucks')

    def get_success_url(self):
        return reverse_lazy('potlucks:vendor_detail', self.object.get_absolute_url)


class VendorDetailView(DetailView):
    #group_required = ['Уровень 0', 'Уровень 1']
    model = Vendor
    slug_field = 'url'
    template_name = 'potlucks/vendors/vendor_detail.html'


class PartOrderListView(ListView):
    queryset = PartOrder.objects.all().order_by('-created')
    context_object_name = 'orders'
    template_name = 'potlucks/parts/part_orders.html'
    paginate_by = 4
    paginate_orphans = 3


class JsonPartOrderFilterListView(ListView):

    template_name = 'potlucks/parts/part_orders_filter.html'
    context_object_name = 'orders'
    paginate_orphans = 3

    def get_paginate_by(self):
        return 5

    def get_queryset(self):
        get_confirmed = self.request.GET.getlist("confirmed")
        get_paid = self.request.GET.getlist("paid")
        request = self.request.GET.get('order_search')

        confirmed_filter = get_confirmed if get_confirmed else (True, False)
        paid_filter = get_paid if get_paid else (True, False)

        queryset = PartOrder.objects.filter(
            confirmed__in=confirmed_filter,
            paid__in=paid_filter
        ).order_by('-created')

        if request:
            print(request)
            print(request.isdigit())
            if request.isdigit():
                queryset = queryset.filter(
                    Q(id__exact=request) |
                    Q(phone_number__exact=request) |
                    Q(post_index__exact=request)
                ).distinct()

            else:
                queryset = queryset.filter(
                    Q(email__contains=request) |
                    Q(notes__iregex=request) |
                    Q(first_name__iregex=request) |
                    Q(last_name__iregex=request) |
                    Q(patronymic__iregex=request) |
                    Q(city__iregex=request) |
                    Q(address__iregex=request)
                ).distinct()

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = {'paginate_by': self.get_paginate_by(), 'orders': {}}
        for order in queryset:
            response['orders'][f'{order.id}'] = {
                'customer': str(order.part.customer.user.email) if order.part.customer else '',
                'first_name': order.first_name,
                'last_name': order.last_name,
                'patronymic': order.patronymic,
                'phone_number': str(order.phone_number),
                'email': order.email,
                'city': order.city,
                'address': order.address,
                'post_index': str(order.post_index),
                'notes': order.notes,
                'created': format_date(order.created),
                'total_cost': str(order.part.total_cost),
                'items': {},
                'confirmed': order.confirmed,
                'paid': order.paid,
                'product': order.part.potluck.product.name,
                'goods_number': str(order.part.goods_number),
                'product_price': str(order.part.potluck.unit_price)

            }
            # for item in order.items.all():
            #     response['orders'][f'{order.id}']['items'][f'{item.id}'] = {
            #         'product': item.product.name,
            #         'quantity': str(item.quantity),
            #         'price': str(item.product.price),
            #         'item_cost': str(item.get_cost),
            #     }
        print("успех")
        return JsonResponse(response, safe=False, status=200)