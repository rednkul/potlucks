from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect

from .utils import format_date


from .models import Product, Rating, Review
from .views import Ratings


def review_and_rate(request, pk):
    review_text = request.POST.get('review-text')
    star = request.POST.get("star")
    product = Product.objects.get(pk=pk)

    review, created = Review.objects.update_or_create(
        product=product,
        customer=request.user.profile,

    )

    review.text += review_text
    review.updated_at = datetime.today() if not created else None

    review.save()

    rating = Rating.objects.update_or_create(
        review=review,
        defaults={'star_id': int(star) if star else 5},
    )

    avg_rating = product.avg_rating


    number_of_ratings = {}

    for verb, value in Ratings.number_of_ratings().items():
        number_of_ratings[f'{verb}'] = Rating.objects.filter(star__value=value,
                                                             review__product=product).count()

    response = {
        "review": {
            "text": review.text,
            "customer": request.user.profile.first_name,
            "star": int(star) if star else 5,
            "date": format_date(review.date),
            "created": created,
            "id": review.id,
            "updated_at": format_date(review.updated_at),
        },
        "product": {
            "rating_avg": avg_rating,
            "number_of_ratings": number_of_ratings,
        },

    }

    return JsonResponse(response, status=200)


