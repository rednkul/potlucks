from django.shortcuts import redirect

from .models import Product, Rating, Review


def review_and_rate(request, pk):

    review_text = request.POST.get('review-text')
    star = request.POST.get("star")
    product = Product.objects.get(pk=pk)

    review = Review.objects.update_or_create(
        product=product,
        text=review_text,
        customer=request.user.profile,
    )


    rating = Rating.objects.update_or_create(

        review=review[0],
        defaults={'star_id': int(star) if star else 5},
    )



    return redirect('goods:product_detail', slug=product.url)

