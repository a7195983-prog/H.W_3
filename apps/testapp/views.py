from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAdminOnly, IsUserOnly
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Поле refresh обязательно.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
        except Exception:
            return Response({'detail': 'Некорректный refresh токен.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(token['user_id']) != str(request.user.id):
            return Response({'detail': 'Этот refresh токен принадлежит другому пользователю.'}, status=status.HTTP_403_FORBIDDEN)

        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ProfileStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'role': user.role,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined,
        })

class AdminOnlyView(APIView):
    permission_classes = [IsAdminOnly]

    def get(self, request):
        return Response({"message": "Добро пожаловать, Admin!"})

class UserOnlyView(APIView):
    permission_classes = [IsUserOnly]

    def get(self, request):
        return Response({"message": "Добро пожаловать, User!"})

    
     

