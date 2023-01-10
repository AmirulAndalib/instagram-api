""" Users views module """

# Python standard library
from typing import Any

# Django REST Framework
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Instagram Models
from instagram.core.models import User
# Instagram serializers
from instagram.apps.users.serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    UserLoginSerializer
)
# Instagram permissions
from instagram.apps.users.permissions import IsAccountOwner


class UserViewSet(mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """User viewset

    This is the view for users that controls main actions
    like create, update, delete, read data and more.
    """

    lookup_field = 'username'

    def get_queryset(self, username: str = None):
        """ Return a queryset type """
        if not username:
            return User.objects.all()

        return User.objects.filter(username=username).first()

    def get_permissions(self):
        """ Add permissions depends on the action """
        permissions = []

        if self.action in ['signup', 'verification', 'login']:
            permissions = [AllowAny]
        elif self.action == 'retrieve':
            permissions = [IsAuthenticated, IsAccountOwner]

        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """ Returns a serializer class depends on the action """
        if self.action == 'signup':
            return UserSignUpSerializer
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'verification':
            return AccountVerificationSerializer
        if self.action == 'retrieve':
            return UserModelSerializer

    @action(detail=False, methods=['POST'])
    def signup(self, request: Request):
        """ Users signup action """
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            data = UserModelSerializer(instance=user).data

            return Response(data=data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def verification(self, request: Request):
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data={ 'message': 'Your account has been verified.' },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request: Request):
        """ Users login action """
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user, token = serializer.save()

            data = {
                'user': UserModelSerializer(instance=user).data,
                'access_token': token
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request: Request, username: str, *args: Any, **kwargs: Any):
        """ Retrieve user data """
        user = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        queryset = self.get_queryset(username = username)

        if queryset:
            return Response(user.data, status=status.HTTP_200_OK)