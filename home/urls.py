from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path("search/", views.search_random, name = "search"),
    path("config_search/", views.search_with_config, name = "searcg_with_config")
]
