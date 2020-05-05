from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.serializers import UserRegisterSerializer, UserDetailSerializer
from custom.views import CustomViewSet
from custom.permissions import IsSelfOrReadOnly
from custom.response import JsonResponse

User = get_user_model()


class UserViewSet(CustomViewSet):

    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    ordering_fields = ('create_at', 'update_at')

    # 动态配置Serializer
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        return [IsSelfOrReadOnly()]


class UserInfoAPIView(GenericAPIView):

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserDetailSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)


get_user_info = UserInfoAPIView.as_view()
