from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from goods.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  update_quantity=cd['update'])
#     return redirect('cart:cart_detail')


def cart_add(request, product_id):

    print(product_id)
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    print('что-то творится тут')
    print(cart.__len__())
    response = {"cart_qty": str(cart.__len__())}
    return JsonResponse(response, status=200)

# def add_product_to_wishlist(request, pk):
#
#
#     wishlist = Wishlist.objects.get(customer=request.user.profile)
#
#     wishlist.products.add(pk)
#
#     wishlist.save()
#
#
#     return JsonResponse({"product": pk}, status=200)

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})