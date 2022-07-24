from django.http import JsonResponse
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
    )[0]


    rating = Rating.objects.update_or_create(

        review=review,
        defaults={'star_id': int(star) if star else 5},
    )

    response = {"review": {
        "text": review_text,
        "customer": request.user.profile.first_name,
        "star": int(star) if star else 5,
        "date": review.date,
    }
                }

    return JsonResponse(response, status=200)

    #return redirect('goods:product_detail', slug=product.url)

