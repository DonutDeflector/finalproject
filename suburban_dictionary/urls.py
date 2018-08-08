from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path("admin", admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("new", views.new_definition, name="new_definition"),
    path("term/<term_name>", views.term, name="term"),
    path("search", views.search_for_term, name="search_for_term"),
    path("like_definition", views.like_definition, name="like_definition"),
    path("dislike_definition", views.dislike_definition, name="dislike_definition"),
    path("user_vote", views.user_vote, name="user_vote"),
    path("edit/<int:definition_id>", views.edit_definition, name="edit_definition"),
    path("delete_definition", views.delete_definition, name="delete_definition")
]
