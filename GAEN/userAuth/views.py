from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, hashers

from .models import CustomUser
from .serializers import CustomUserSerializer
from . import randomCode, codeSendToMail


# path('signUp/',),
class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email is None:
            return Response({'message': 'email required'})
        ex_user = CustomUser.objects.filter(email=email).first()
        if ex_user:
            return Response({'message': f'{email} already has registered'})
        password = request.data.get('password')
        if password is None:
            return Response({'message': 'password must not be empty'})
        elif len(password) < 9:
            return Response({'message': 'password must be at least 8 char'})
        code = randomCode.get_random_code()
        code = str(123456)
        is_success = codeSendToMail.send_email('muxtorovshaxzodbek16@gmail.com', "xuoz qigk ipia wifm",
                                               to_email='abroyevmuslimbek@gmail.com', message=code)
        if not is_success:
            return Response({'message': 'server error'})
        conf_code = request.data.get('conf_code')
        if conf_code != code:
            return Response({'message': 'Incorrect code'})
        first_name = request.data.get('first_name')
        if first_name is None:
            return Response({'message': 'first_name required'})
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        profile_pic = request.data.get('profile_pic')
        country = request.data.get('country')
        if country is None:
            return Response({'message': 'country required'})
        user = CustomUser.objects.create(email=email, password=hashers.make_password(password), conf_code=conf_code,
                                         first_name=first_name, last_name=last_name, username=username,
                                         profile_pic=profile_pic, country=country)
        token = RefreshToken.for_user(user)
        return Response({
            'message': f'Successfully created by {email}',
            'user': CustomUserSerializer(user).data,
            'access_token': str(token.access_token),
            'refresh_token': str(token)
        })


# path('logIn/',),

class LogInAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email is None or email == '':
            return Response({'message': 'email must not be empty'}, status=status.HTTP_200_OK)
        password = request.data.get('password')
        try:
            user = CustomUser.objects.filter(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message': f'{email} has not registered yet'}, status=status.HTTP_404_NOT_FOUND)
        if password is None:
            return Response({'message': 'Password must not be empty'})
        user = authenticate(email=email, password=password)

        if user is not None:
            return Response({'message': f'Hello {user.first_name}, Welcome to GAEN!'})
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


# path('logOut/'),
class LogOutAPIView(APIView):
    pass

# path('resetPassword/'),
# path('resendCode/'),
