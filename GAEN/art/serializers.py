from rest_framework import serializers
from .models import Category, Art, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArtSerializer(serializers.ModelSerializer):
    class Mete:
        model = Art
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
