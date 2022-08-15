"""potluck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.flatpages import views

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),

    path('cart/', include('cart.urls')),
    path('retail/', include('retail.urls')),
    path('potlucks/', include('potlucks.urls')),
    path('accounts/', include('allauth.urls')),
    path('ajax/', include('ajax.urls')),
    path('users/', include('users.urls')),
    path('', include('goods.urls')),

]

urlpatterns += [
    path('about_us/', views.flatpage, {'url':'/about_us/'}, name='about_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)