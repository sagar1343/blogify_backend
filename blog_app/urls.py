from django.urls import path

from . import views

urlpatterns = [
    path('blogs/', views.BlogView.as_view()),
    path('blogs/<int:pk>', views.BlogDetailView.as_view()),
    path('categories/', views.CategoryView.as_view())
]
