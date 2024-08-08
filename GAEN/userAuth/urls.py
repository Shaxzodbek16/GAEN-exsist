from django.urls import path
from .views import RegisterAPIView, LogInAPIView

urlpatterns = [
    path('signUp/', RegisterAPIView.as_view(), name='register'),
    path('logIn/', LogInAPIView.as_view(), name='login'),
    # path('logOut/'),
    #
    # path('resetPassword/'),
    # path('resendCode/'),
    #
    # path('updateInfo/'),
]
