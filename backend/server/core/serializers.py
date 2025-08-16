# myapp/serializers.py
from djoser.serializers import UserSerializer as BaseUserSerializer

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = tuple(BaseUserSerializer.Meta.fields) + ('first_name', 'last_name')  # Add extra fields