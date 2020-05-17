from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from action.models import Like, Fav, Comment, Reply, Message
from action.serializers import LikeSerializer, FavSerializer, CommentSerializer, CommentDetailSerializer
from action.serializers import ReplySerializer, ReplyDetailSerializer, MessageSerializer
from custom.permissions import IsCreatorOrReadOnly, IsReceiverOrReadOnly, IsSelfOrReadOnly
from custom.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from utils.tools import get_client_ip


# Create your views here.


class LikeViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """
    create: 点赞
    delete: 取消点赞
    """
    permission_classes = (IsAuthenticated, IsSelfOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user.id)


class FavViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    list: 收藏列表
    create: 添加收藏
    delete: 取消收藏
    retrieve: 收藏详情
    """
    permission_classes = (IsAuthenticated, IsCreatorOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    serializer_class = FavSerializer

    def get_queryset(self):
        return Fav.objects.filter(user=self.request.user.id)


class CommentViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    list: 评论列表
    create: 添加评论
    delete: 删除评论
    retrieve: 评论详情
    """
    queryset = Comment.objects.all().order_by('-create_at')
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsCreatorOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('article', )

    # 动态配置Serializer
    serializer_class = CommentDetailSerializer

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id)


class ReplyViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    list: 回复列表
    create: 添加回复
    delete: 删除回复
    retrieve: 回复详情
    """
    queryset = Reply.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsReceiverOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('comment',)

    serializer_class = ReplyDetailSerializer

    def perform_create(self, serializer):
        receiver_id = serializer.validated_data['receiver_id']
        serializer.save(creator_id=self.request.user.id, receiver_id=receiver_id)


class MessageViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    list: 留言列表
    create: 添加留言
    """
    queryset = Message.objects.all().order_by('-create_at')
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        user_ip = get_client_ip(self.request)
        anonymous = serializer.validated_data['anonymous']
        if anonymous:
            serializer.save(creator_id=1, creator_ip=user_ip)
        else:
            serializer.save(creator_id=self.request.user.id, creator_ip=user_ip)
