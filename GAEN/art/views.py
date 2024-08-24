from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from .models import Art, Category, Comment
from .serializers import ArtSerializer, CategorySerializer, CommentSerializer

from userAuth.models import User
from userAuth.serializers import UserSerializer


class CategoryAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, slug=None):
        if slug:
            try:
                category = Category.objects.get(slug=slug)
                return Response(data={'category': CategorySerializer(category).data})
            except:
                return Response({'message': f'Category not found by {slug}'})
        categories = Category.objects.all()
        return Response(data=CategorySerializer(categories, many=True).data)

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')

        if name is None:
            return Response({'message': 'Category name must not be empty'})
        if name.strip() == '':
            return Response({'message': 'Category name must not be just whitespace'})
        ex_name = Category.objects.filter(name=name).first()
        if ex_name:
            return Response({'message': f'Category {name} is already added'})
        category = Category.objects.create(name=name, description=description)
        return Response(data={
            'message': f'Category successfully created by {name} name',
            'category': CategorySerializer(category).data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, slug=None):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({"error": f"category not found by {slug}"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug=None):
        try:
            category = Category.objects.get(slug=slug)
            category.delete()
            return Response({"message": f"{category.name} category successfully deleted"})
        except Category.DoesNotExist:
            return Response({"error": f"category not found by {slug} id"}, status=status.HTTP_404_NOT_FOUND)


class ArtAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly or permissions.IsAdminUser]

    def get(self, request, slug=None):
        user = request.user
        if user.is_authenticated:
            arts = Art.objects.filter(user=user)
        else:
            arts = Art.objects.all()

        if slug:
            try:
                art = arts.get(slug=slug)
                return Response(ArtSerializer(art).data, status=status.HTTP_200_OK)
            except Art.DoesNotExist:
                return Response(data={'message': f'Art with ID {slug} not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ArtSerializer(arts, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(data={'message': 'Authentication required to create art'},
                            status=status.HTTP_401_UNAUTHORIZED)

        title = request.data.get("title")
        description = request.data.get("description")
        art_img = request.data.get("art_img")
        category = request.data.get("category")

        if title is None or title.strip() == '':
            return Response(data={'message': 'Title required'})
        if art_img is None or art_img.strip() == '':
            return Response(data={'message': 'art_img required'})
        if category is None or category.strip() == '':
            return Response(data={'message': 'category required'})

        category = category.strip()
        try:
            category_obj = Category.objects.get(name=category)
        except Category.DoesNotExist:
            return Response(data={'message': 'Unknown category'})

        new_art = Art(
            title=title, description=description, art_img=art_img,
            category=category_obj, user=user
        )
        new_art.save()

        return Response(ArtSerializer(new_art).data, status=status.HTTP_201_CREATED)

    def put(self, request, slug=None):
        try:
            art = Art.objects.get(slug=slug)
        except Art.DoesNotExist:
            return Response(data={'message': f'Art with ID {slug} not found'}, status=status.HTTP_404_NOT_FOUND)

        if art.user == request.user or request.user.is_superuser:
            title = request.data.get("title", art.title)
            description = request.data.get("description", art.description)
            art_img = request.data.get("art_img")
            category = request.data.get("category")

            if art_img:
                art.art_img = art_img
            if category:
                category = category.strip()
                if category:
                    try:
                        category_obj = Category.objects.get(name=category)
                        art.category = category_obj
                    except Category.DoesNotExist:
                        return Response(data={'message': 'Unknown category'})
            if title != art.title:
                art.title = title
            if description != art.description:
                art.description = description
            art.edited = True
            art.save()
            return Response(ArtSerializer(art).data, status=status.HTTP_200_OK)
        return Response(data={'message': 'You can only update your own art'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, slug=None):
        try:
            art = Art.objects.get(slug=slug)
        except Art.DoesNotExist:
            return Response(data={'message': f'Art with ID {slug} not found'}, status=status.HTTP_404_NOT_FOUND)

        if art.user != request.user:
            return Response(data={'message': 'You can only delete your own art'}, status=status.HTTP_403_FORBIDDEN)
        art.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GlobalArtApiView(APIView):
    permissions = [permissions.AllowAny]

    def get(self, request, slug=None):
        arts = Art.objects.all()
        if slug:
            try:
                art = arts.get(slug=slug)
                return Response(data={"message": ArtSerializer(art).data}, status=status.HTTP_200_OK)
            except Art.DoesNotExist:
                return Response(data={'message': f'Not found by {slug} id'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ArtSerializer(arts, many=True).data, status=status.HTTP_200_OK)


class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, comment_slug=None, *args, **kwargs):
        try:
            art = Art.objects.get(slug=self.kwargs['art_slug'])
        except Art.DoesNotExist:
            return Response(data={'message': 'Given art does not exist'}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.all().filter(art=art)
        if comment_slug:
            try:
                return Response({f"comments to {art.title}": CommentSerializer(comments.get(slug=comment_slug)).data})
            except:
                return Response(data={'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            art = Art.objects.get(slug=self.kwargs['art_slug'])
        except Art.DoesNotExist:
            return Response(data={'message': 'Given art does not exist'}, status=status.HTTP_404_NOT_FOUND)
        user_obj = request.user

        text = request.data.get("text")
        if text is None:
            return Response(data={'message': 'text must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        text = text.strip()
        if text == '':
            return Response(data={'message': 'text must not include only white spaces'},
                            status=status.HTTP_400_BAD_REQUEST)

        comment_obj = Comment(text=text, user=user_obj, art=art)
        comment_obj.save()
        return Response(data={
            'comment': CommentSerializer(comment_obj).data,
            'user': UserSerializer(user_obj).data,
            "art": ArtSerializer(art).data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, comment_slug=None, *args, **kwargs):
        try:
            art = Art.objects.get(slug=self.kwargs['art_slug'])
        except Art.DoesNotExist:
            return Response(data={'message': 'Given art does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not comment_slug:
            return Response({"message": "select comment"}, status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(slug=comment_slug)
        except Comment.DoesNotExist:
            return Response({"message": "comment not found"}, status.HTTP_404_NOT_FOUND)
        new_text = request.data.get('text')
        if new_text is None:
            return Response({'message': 'text must not be empty for edit'})
        new_text = new_text.strip()
        if new_text == '':
            return Response({'message': 'text must not include only white space'})
        if new_text == comment.text:
            return Response({'message': 'No changes detected'})
        comment.text = new_text
        comment.edited = True
        comment.save()

        return Response({'new_comment': CommentSerializer(comment).data}, status=status.HTTP_200_OK)

    def delete(self, request, comment_slug=None, *args, **kwargs):
        try:
            art = Art.objects.get(slug=self.kwargs['art_slug'])
        except Art.DoesNotExist:
            return Response(data={'message': 'Given art does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not comment_slug:
            return Response({"message": "select comment"}, status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(slug=comment_slug)
        except Comment.DoesNotExist:
            return Response({"message": "comment not found"}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({'message': 'You can only delete your own comments'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
