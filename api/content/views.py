from datetime import datetime

from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from custom.views import CustomViewSet
from custom.response import JsonResponse
from custom.permissions import IsCreatorOrReadOnly
from custom.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from content.serializers import CategorySerializer, ArticleSerializer, ArchiveSerializer, ArticleListSerializer
from content.serializers import TagSerializer, ProfileSerializer, SentenceSerializer
from content.models import Category, Article, Sentence
from content.filters import ArticleFilter

# Create your views here.


class SentenceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):

    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    pagination_class = None


class CategoryViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    list: 文章分类列表页
    create: 创建一个文章类别
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    authentication_classes = ()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser(), IsCreatorOrReadOnly()]
        return [IsCreatorOrReadOnly()]


class ArticleViewSet(CustomViewSet):
    """
    list: 文章列表
    create: 添加一个文章
    update: 更新一个文章
    delete: 删除一个文章
    retrieve: 文章详情
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('update_at', 'like_nums')
    filter_class = ArticleFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer

    def get_queryset(self):
        values = ('id', 'title', 'image', 'category__title', 'update_at')
        if self.action == 'list':
            return Article.objects.values(*values).all().order_by('-update_at')
        return Article.objects.all().order_by('-update_at')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser(), IsCreatorOrReadOnly()]
        return [IsCreatorOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id, category_id=1)

    def retrieve(self, request, *args, **kwargs):
        # 重写查看详情逻辑，每次查看详情，该文章阅读数加1
        instance = self.get_object()
        instance.view_nums += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)

    def update(self, request, *args, **kwargs):
        # 重写更新逻辑，只有当文章内容发生改变时，才修改文章的更新时间
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if len(request.data['content']) != len(instance.content):
            instance.update_at = datetime.now()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(serializer.data)


class ProfileAPIView(GenericAPIView):
    """
    list: 文章简介列表
    """
    queryset = Article.objects.values('id', 'title', 'profile', 'tags', 'update_at').all().order_by('-update_at')
    serializer_class = ProfileSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)


class ArchiveAPIView(GenericAPIView):
    """
    文章归档
    """
    queryset = Article.objects.values('create_at').all()
    serializer_class = ArchiveSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        # 重写查看列表逻辑，返回由年份和月份组成的一个datetime类型的集合
        queryset = self.filter_queryset(self.get_queryset())

        time_list = [f'{item["create_at"].year}-{item["create_at"].month}' for item in queryset]

        serializer = ArchiveSerializer([{'archive': item} for item in set(time_list)], many=True)

        return JsonResponse(serializer.data)


class TagAPIView(GenericAPIView):
    """
    文章Tag
    """
    queryset = Article.objects.values('tags').all()
    serializer_class = TagSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        # 重写查看列表逻辑，提取并返回所有文章的tag
        queryset = self.filter_queryset(self.get_queryset())

        tag_list = []
        for item in queryset:
            if item.tags is not None:
                tag_list += [{'tag': tag} for tag in item['tags'].split(',')]

        serializer = self.get_serializer(tag_list, many=True)

        return JsonResponse(serializer.data)


get_article_profiles = ProfileAPIView.as_view()
get_article_archives = ArchiveAPIView.as_view()
get_article_tags = TagAPIView.as_view()
