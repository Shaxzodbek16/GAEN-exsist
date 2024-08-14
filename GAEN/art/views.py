from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from .models import Art, Category, Comment
from .serializers import ArtSerializer, CategorySerializer, CommentSerializer


class CategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(pk=pk)
                return Response(data={'category': CategorySerializer(category).data})
            except:
                return Response({'message': f'Category not found by {pk}'})
        categories = Category.objects.all()
        return Response(data=CategorySerializer(categories, many=True).data)

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')

        if name is None:
            return Response({'message': 'Category name must not be empty'})
        ex_name = Category.objects.filter(name=name).first()
        if ex_name:
            return Response({'message': f'Category {name} is already added'})
        category = Category.objects.create(name=name, description=description)
        return Response(data={
            'message': f'Category successfully created by {name} name',
            'category': CategorySerializer(category).data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": f"category not found by {pk}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({"message": f"{category.name} category successfully deleted"})
        except Category.DoesNotExist:
            return Response({"error": f"category not found by {pk} id"}, status=status.HTTP_404_NOT_FOUND)


class CommentAPIView(APIView):
    pass


class ArtAPIView(APIView):
    pass
