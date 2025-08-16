# myapp/serializers.py
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserReadSerializer
from django.contrib.auth import get_user_model
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = tuple(BaseUserSerializer.Meta.fields) + ('first_name', 'last_name')  # Add extra fields


User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")

    # If you have a custom UserManager that ignores **extra_fields**, force the fields explicitly:
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=validated_data.get("password"),
        )
        return user

class UserReadSerializer(BaseUserReadSerializer):
    class Meta(BaseUserReadSerializer.Meta):
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")