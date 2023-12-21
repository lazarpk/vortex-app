from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework import status, generics, mixins, permissions


class RegisterUser(mixins.CreateModelMixin, generics.GenericAPIView):
    """Register new user."""
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class UserInfo(APIView):
    """Retreive data of logged in user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

