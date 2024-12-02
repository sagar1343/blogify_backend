from django.urls import path
from .views import UpvoteView

urlpatterns = [
    path('<int:pk>', UpvoteView.as_view(), name='upvote'),
]
