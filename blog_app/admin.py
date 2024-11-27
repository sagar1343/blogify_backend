from django.contrib import admin
from .models import Blog, Category


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "read_by"]
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_per_page = 20
