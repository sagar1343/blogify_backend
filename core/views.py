from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User
from core.serializers import UserPatchSerializer, UserCreationSerializer


# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserCreationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    pagination_class = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(data={
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_picture_url': user.profile_picture_url if user.profile_picture_url else None,
            },
           **tokens
        }, status=status.HTTP_201_CREATED)


class UserPatchView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserPatchSerializer
    permission_classes = [IsAuthenticated]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)