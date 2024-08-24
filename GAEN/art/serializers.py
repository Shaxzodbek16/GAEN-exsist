from dataclasses import field, fields
from tabnanny import filename_only

from rest_framework import serializers
from .models import Category, Art, Comment
from userAuth.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'update_at')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, )

    class Meta:
        model = Comment
        fields = ('text', 'art', 'user', 'created_at')

    def create(self, validated_data):
        comment = Comment.objects.create(text=validated_data["text"], user=validated_data["user"])
        return comment


class ArtSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Art
        fields = ('title', 'art_name', 'country', 'email', 'description', 'art_img', 'category', 'is_accepted',
                  'created_at', 'update_at', 'edited', 'user', 'comments')
