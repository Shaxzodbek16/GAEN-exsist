from django.urls import path
from .views import RegisterAPIView

urlpatterns = [
    path('signUp/', RegisterAPIView.as_view(), name='register'),
    # path('logIn/',),
    # path('logOut/'),
    #
    # path('resetPassword/'),
    # path('resendCode/'),
    #
    # path('updateInfo/'),
]
