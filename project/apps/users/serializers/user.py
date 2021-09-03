from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uuid',
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'birth_date'
        )
        read_only_fields = ('uuid',)


class UserShortNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uuid',
            'username',
            'first_name',
            'last_name',
            'middle_name',
        )
        read_only_fields = ('uuid',)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uuid',
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'birth_date',
        )
        extra_kwargs = {
            'uuid': {'read_only': True},
            'username': {'read_only': True},
            'first_name': {'required': False, 'allow_null': False, 'allow_blank': False},
            'last_name': {'required': False, 'allow_null': False, 'allow_blank': False}
        }


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        validators=[validate_password],
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'last_name',
            'first_name',
            'password'
        )
        extra_kwargs = {
            'username': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'password',
        )

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance, validated_data
