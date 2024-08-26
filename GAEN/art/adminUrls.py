from django.urls import path

from .adminView import AdminCategoryAPIView, AdminArtAPIView, AdminCommentAPIView

urlpatterns = [
    path('category/<str:slug>/', AdminCategoryAPIView.as_view(), name='category'),
    path('category/', AdminCategoryAPIView.as_view(), name='category-create'),
    path('art/', AdminArtAPIView.as_view(), name='get-arts'),
    path('art/<str:slug>/', AdminArtAPIView.as_view(), name='get-art'),
    path('art/<str:art_slug>/comments/', AdminCommentAPIView.as_view(), name='get-arts'),
    path('art/<str:art_slug>/comments/<str:comment_slug>', AdminCommentAPIView.as_view(), name='get-arts'),
]
