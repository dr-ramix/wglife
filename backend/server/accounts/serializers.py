from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile
from core.serializers import UserSerializer

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Profile
        fields = ["user_id","username","email","first_name", "last_name","gender", "birth_date", "profile_picture", "grade"]


class UserDetailSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]

    def update(self, instance, validated_data):
        # Handle nested profile update
        profile_data = validated_data.pop("profile", {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            Profile.objects.update_or_create(user=instance, defaults=profile_data)
        return instance