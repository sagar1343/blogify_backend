from django.urls import path, include

from . import views

urlpatterns = [
    path('blogs/', views.BlogView.as_view()),
    path('blogs/<int:pk>', views.BlogDetailView.as_view()),
    path('blogs/me', views.UsersBlogView.as_view()),
    path('categories/', views.CategoryView.as_view())
]
