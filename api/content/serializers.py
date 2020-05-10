from rest_framework import serializers
from django.contrib.auth import get_user_model

from action.models import Like, Fav
from content.models import Category, Article, Sentence
from user.serializers import UserDetailSerializer


User = get_user_model()


class SentenceSerializer(serializers.ModelSerializer):

    lines = serializers.SerializerMethodField()

    def get_lines(self, obj):
        return obj.lines.split(' ')

    class Meta:
        model = Sentence
        fields = ('id', 'lines')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title', 'info')


class ArchiveSerializer(serializers.Serializer):

    archive = serializers.CharField(read_only=True)


class TagSerializer(serializers.Serializer):

    tag = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'profile', 'tags', 'update_at')


class ArticleListSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj['category__title']

    class Meta:
        model = Article
        fields = ('id', 'title', 'image', 'category', 'update_at')


class ArticleSerializer(serializers.ModelSerializer):

    is_like = serializers.SerializerMethodField()
    is_fav = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_creator(self, obj):
        user = UserDetailSerializer(obj.creator, context={'request': self.context['request']})
        return user.data

    def get_is_like(self, obj):
        user = self.context['request'].user
        if not isinstance(user, User):
            return False
        like = Like.objects.filter(user=user, like_id=obj.id, like_type='article').first()
        if not like:
            return False
        return like.id

    def get_is_fav(self, obj):
        user = self.context['request'].user
        if not isinstance(user, User):
            return False
        fav = Fav.objects.filter(user=user, article=obj).first()
        if not fav:
            return False
        return fav.id

    def get_is_author(self, obj):
        user = self.context['request'].user
        return user == obj.creator

    def get_category(self, obj):
        return obj.category.title

    class Meta:
        model = Article
        exclude = ('create_at', 'delete_at')
