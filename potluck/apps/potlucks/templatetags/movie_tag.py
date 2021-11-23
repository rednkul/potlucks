from django import template

from potlucks.models import Category, Vendor, Manufacturer

register = template.Library()

@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()

# @register.simple_tag()
# def get_genres():
#     """Жанры фильмов"""
#     return Genre.objects.all()
#
# @register.simple_tag()
# def get_years():
#     """Года выхода фильмов"""
#     return Movie.objects.filter(draft=False).values_list("year", flat=True).distinct()

@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count=5):
    """Вывод послених 5 фильмов"""
    movies = Movie.objects.filter(draft=False).order_by('-id')[:count]
    return {'last_movies': movies}



