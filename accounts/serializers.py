from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "name", "email", "password")
        read_only_fields = ("id",)

    def validate_email(self, value):
        return value.lower().strip()

    def create(self, validated_data):
        email = validated_data["email"]
        username = email
        return User.objects.create_user(
            username=username,
            email=email,
            name=validated_data["name"].strip(),
            password=validated_data["password"],
        )
