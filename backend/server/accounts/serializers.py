from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model, including related User fields.
    """
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name  = serializers.CharField(source="user.last_name",  required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = [
            "user_id", "username", "email",
            "first_name", "last_name",
            "gender", "birth_date", "profile_picture", "grade", "telephone"
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
   
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related User fields, if provided
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save(update_fields=list(user_data.keys()))

        return instance

    def create(self, validated_data):
        # If you ever create via this serializer, decide how to pick the user.
        # Commonly: attach to request.user (requires context={'request': request})
        user_data = validated_data.pop("user", None)  # ignore unexpected nested user on create
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Cannot create profile without an authenticated user.")
        return Profile.objects.create(user=user, **validated_data)