# tribes/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import People, Favorite, Comment

class PeopleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug')

    class Meta:
        model = People
        fields = ['id', 'name', 'region', 'description', 'culture', 'images', 'language', 'traditions', 'audio', 'history']  # Добавляем history

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    people = PeopleSerializer(read_only=True)
    people_slug = serializers.SlugField(source='people.slug', write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'people', 'people_slug', 'added_at']

class UserProfileSerializer(serializers.ModelSerializer):
    favorites = FavoriteSerializer(many=True, read_only=True, source='favorite_set')
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'favorites', 'comments']

    def validate_username(self, value):
        if User.objects.exclude(pk=self.instance.pk).filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value