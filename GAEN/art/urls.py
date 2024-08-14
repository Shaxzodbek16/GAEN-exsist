from django.urls import path

from .views import CategoryAPIView, CommentAPIView, ArtAPIView

urlpatterns = [
    path('category/<int:pk>/', CategoryAPIView.as_view(), name='category'),
    path('category/', CategoryAPIView.as_view(), name='category-create'),

    path('comment/<int:pk>/', CommentAPIView.as_view(), name='comment'),
    path('comment/', CommentAPIView.as_view(), name='create-comment'),

    path('art/<int:pk>/', ArtAPIView.as_view(), name='art'),
    path('art/', ArtAPIView.as_view(), name='create-art')
]
