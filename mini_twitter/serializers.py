from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Este email já está em uso. Tente outro e-mail.'
            )
        ]
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        errors = {}

        try:
            validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', instance.password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.set_password(password)
        instance.save()

        return instance

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
