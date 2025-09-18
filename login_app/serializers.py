from rest_framework import serializers
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'profile_picture',
            'username',
            'full_name',
            'address_1',
            'city',
            'zipcode',
            'country',
            'phone',
            'date_joined',
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # Profile nested

    class Meta:
        model = User
        # fields = ['id', 'email', 'is_active', 'is_staff', 'profile']
        fields = ['id','phone', 'email', 'is_active', 'is_staff', 'profile']
        read_only_fields = ['is_staff', 'is_active']


class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, min_length=6)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "phone", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # ✅ password hash করে save
        user.save()
        return user