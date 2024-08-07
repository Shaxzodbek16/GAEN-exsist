from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, hashers

from .models import CustomUser
from . import randomCode, codeSendToMail


# path('signUp/',),
class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        ex_user = CustomUser.objects.filter(email=email).first()
        if ex_user:
            return Response({'message': f'{email} already has registered'})
        code = randomCode.get_random_code()
        code = str(123456)
        codeSendToMail.send_email('muxtorovshaxzodbek16@gmail.com', "xuoz qigk ipia wifm",
                                  to_email='abroyevmuslimbek@gmail.com', message=code)
        conf_code = request.data.get('conf_code')
        if conf_code != code:
            return Response({'message': 'Incorrect code'})
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        profile_pic = request.data.get('profile_pic')
        country = request.data.get('country')
        user = CustomUser.objects.create(email=email, password=hashers.make_password(password), conf_code=conf_code,
                                         first_name=first_name, last_name=last_name, username=username,
                                         profile_pic=profile_pic, country=country)
        token = RefreshToken.for_user(user)
        return Response({
            'message': f'Successfully created by {email}',
            'access_token': str(token.access_token),
            'refresh_token': str(token)
        })


# path('logIn/',),
class LogInAPIView(APIView):
    pass


# path('logOut/'),
class LogOutAPIView(APIView):
    pass

# path('resetPassword/'),
# path('resendCode/'),
# path('updateInfo/'),
