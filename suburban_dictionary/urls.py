from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path("admin", admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("create_definition", views.create_definition, name="create_definition"),
    path("term/<term_name>", views.term, name="term"),
    path("search", views.search_for_term, name="search_for_term"),
    path("like_definition", views.like_definition, name="like_definition")
]
