from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/<int:project_id>/", views.project_detail, name="project_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("category/", views.category_view, name="Category"),
    path("todo/", views.todo_view, name="TodoList"),
]