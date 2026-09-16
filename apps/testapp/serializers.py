from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds the authenticated user's data to the standard JWT token response."""

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role,
        }
        return data
