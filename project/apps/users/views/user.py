from django.db.models.deletion import ProtectedError
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework.validators import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from users.models import User
from users.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserChangePasswordSerializer)
from users.filters import UserFilter


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'middle_name']

    def get_serializer_class(self):
        serializer_class = UserSerializer

        if self.action == 'create':
            serializer_class = UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            serializer_class = UserUpdateSerializer
        elif self.action in ['change_my_password', 'change_user_password']:
            serializer_class = UserChangePasswordSerializer

        return serializer_class

    def get_permissions(self):
        if self.action in ['create', 'auth']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError({
                "non_field_errors": ["Нельзя удалить пользователи так как к ней привязаны другие данные."]
            })
        return Response(status=200)

    @action(methods=['GET'], detail=False, url_path='me')
    def me(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)

    @action(methods=['POST'], detail=False, url_path='change_password')
    def change_my_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True})

    @action(methods=['POST'], detail=True, url_path='change_password')
    def change_user_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True})


class ObtainAuthToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
