from django.urls import path
from . import views


app_name = "post"

urlpatterns = [
    path("", views.posts, name="posts"),
    path("<uuid:id>", views.post_detail, name="post_detail"),
    path("add", views.add_post, name="add_post"),
    path("edit/<uuid:id>", views.edit_post, name="edit_post"),
    path("delete/<uuid:id>", views.delete_post, name="delete_post"),
    path("comment/<uuid:id>", views.add_comment, name="add_comment"),
]
