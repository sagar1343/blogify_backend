from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.BlogView.as_view()),
    path("<int:pk>", views.BlogDetailView.as_view()),
    path("me", views.UsersBlogView.as_view()),
    path("categories", views.CategoryView.as_view()),
]
