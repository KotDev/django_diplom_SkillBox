import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Avatar
from .serializers import ProfileSerializer, ChangePasswordSerializer


class SignInView(APIView):
    """View для входа в профиль"""

    def post(self, request: HttpRequest) -> Response:
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")  # Получаем username
        password = user_data.get("password")  # Получаем пароль
        user = authenticate(request, username=username, password=password)  # Аунтифицируем пользователя

        if user is not None:
            login(request, user)  # Логиним пользователя
            return Response(
                status=status.HTTP_201_CREATED)  # статусы такие берутся от сюда from rest_framework import status

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """View для регистрации пользователя"""

    def post(self, request: HttpRequest) -> Response:
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get('name')  # Получаем имя пользователя
        username = user_data.get('username')  # Получаем username
        password = user_data.get('password')  # Получаем пароль
        try:
            user = User.objects.create_user(username=username, password=password)  # Создаём пользователя
            Profile.objects.create(user=user, fullName=name)  # Создаём профиль пользователя
            user = authenticate(request, username=username, password=password)  # Аунтифицируем пользователя
            login(request, user)  # Логиним пользователя
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignOutView(APIView):
    """View для выхода из профиля"""

    def post(self, request: HttpRequest) -> Response:
        logout(request)  # Выход пользователя
        return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    """View дял профиля пользователя"""

    permission_classes = [permissions.IsAuthenticated]  # Проверяем аунтифицирован ли пользователь

    def get(self, request: HttpRequest) -> Response:
        profile = Profile.objects.get(user=request.user)  # Получаем текущего пользователя
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        profile = Profile.objects.get(user=request.user)  # Получаем текущего пользователя
        serializer = ProfileSerializer(profile, data=request.data, partial=True)  # Сериализуем данные
        if serializer.is_valid():
            serializer.save()  # Сохраняем данные в db
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """View для изменения пароля"""

    def post(self, request: HttpRequest) -> Response:
        user = User.objects.get(username=request.user.username)  # Получаем текущего пользователя
        serializer = ChangePasswordSerializer(instance=user, data=request.data)  # Сериализуем данные
        if serializer.is_valid():
            serializer.save()  # Сохраняем данные в db
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAvatarView(APIView):
    """View для изменения аватара пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest) -> Response:
        image = request.FILES["avatar"]  # Получаем данные аватара
        profile = Profile.objects.get(user=request.user)  # Получаем текущий профиль
        if 'default-avatar.jpg' not in str(profile.avatar.src):  # Проверяем дефолд аватар
            profile.avatar.src.delete(save=False)  # Удаляем текущий аватар пользователя
        profile.avatar.delete()
        if str(image).lower().endswith(('jpg', 'png', 'jpeg')):  # Проверяем аватар на разрешение
            avatar = Avatar.objects.create(src=image)  # Создаём аватар
            profile.avatar = avatar  # Изменяем аватар
            profile.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
