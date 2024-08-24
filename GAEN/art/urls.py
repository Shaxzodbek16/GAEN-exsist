from django.urls import path

from .views import CategoryAPIView, CommentAPIView, ArtAPIView, GlobalArtApiView

urlpatterns = [
    path('category/<str:slug>/', CategoryAPIView.as_view(), name='category'),
    path('category/', CategoryAPIView.as_view(), name='category-create'),

    path('art/', ArtAPIView.as_view(), name='get-arts'),
    path('art/<str:slug>/', ArtAPIView.as_view(), name='get-art'),

    path('art-for-all/', GlobalArtApiView.as_view(), name='global-get'),
    path('art-for-all/<str:slug>/', GlobalArtApiView.as_view(), name='global-get'),

    path('art/<str:art_slug>/comments/', CommentAPIView.as_view(), name='get-arts'),
    path('art/<str:art_slug>/comments/<str:comment_slug>', CommentAPIView.as_view(), name='get-arts'),

]
