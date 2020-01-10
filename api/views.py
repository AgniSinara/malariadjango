from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    user_type = {
        1: 'Dokter',
        2: 'Tenaga Medis',
        3: 'Pasien'
    }
    full_name = user.first_name + ' ' + user.last_name

    return Response({
        'token': token.key,
        'userId': user.pk,
        'username': user.username,
        'fullName': full_name,
        'userType': user_type[user.profile.user_type]
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    first_name = request.data.get('firstName')
    last_name = request.data.get('lastName')
    user_type = request.data.get('userType')

    user_serializers = UserSerializer(data=request.data)
    if user_serializers.is_valid() and user_type in [1, 2, 3]:
        user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name)

        user.profile.user_type = user_type
        user.save()

        return Response({
            'status': 1,
            'message': 'User successfully created'
        })
    else:
        return Response({
            'status': 0,
            'message': 'Please provide all required data'
        }, status=HTTP_400_BAD_REQUEST)




@csrf_exempt
@api_view(["GET"])
def my_profile(request):
    user = request.user
    username = user.username
    user_type = user.profile.user_type
    full_name = user.first_name + ' ' + user.last_name

    return Response({
        'username': username,
        'fullName': full_name,
        'userType': user_type
    }, status=HTTP_200_OK)

