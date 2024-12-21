from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from mini_twitter.models import Comment, Post


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


class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post_id = serializers.PrimaryKeyRelatedField(
        source='post',
        queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'author', 'post_id', 'created_at', 'updated_at']


class CommentRetrieveUpdateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post_id = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'author', 'post_id', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentRetrieveUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'author',
            'total_comments',
            'comments',
            'created_at',
            'updated_at',
        ]
