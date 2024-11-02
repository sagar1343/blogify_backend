from django.urls import path
from .views import UserCreationView, UserPatchView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserCreationView.as_view(), name='register'),
    path('<int:pk>', UserPatchView.as_view(), name='user-detail'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

