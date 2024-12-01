from django.urls.conf import path
from .views import CommentView

urlpatterns = [path("<int:pk>", CommentView.as_view())]
