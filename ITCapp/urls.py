from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.login),
    path("register", views.register),
    path("recommend", views.recommend),
    path("about", views.about),
    path("search", views.search),
    path("update", views.search),
    path("home", views.home)
]
