from django.contrib.auth import get_user_model
from rest_framework import serializers

from action.models import Like, Fav, Comment, Reply, Message
from user.serializers import UserDetailSerializer


User = get_user_model()


class FavSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Fav
        fields = ('article', 'user')


class LikeSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('like_id', 'like_type', 'user')


class ReplySerializer(serializers.ModelSerializer):

    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    like_nums = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reply
        fields = ('comment', 'receiver', 'creator', 'content', 'like_nums')


class ReplyDetailSerializer(serializers.ModelSerializer):

    receiver_id = serializers.IntegerField()
    creator = UserDetailSerializer(read_only=True)
    receiver = UserDetailSerializer(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)

    def get_is_like(self, obj):
        user = self.context['request'].user
        if not isinstance(user, User):
            return False
        like = Like.objects.filter(user=user, like_id=obj.id, like_type='reply').first()
        if not like:
            return False
        return like.id

    def get_creator(self, obj):
        user = User.objects.filter(id=obj.creator_id)[0]
        creator_serializer = UserDetailSerializer(user, context={'request': self.context['request']})
        return creator_serializer.data

    def get_receiver(self, obj):
        user = User.objects.filter(id=obj.receiver_id)[0]
        receiver_serializer = UserDetailSerializer(user, context={'request': self.context['request']})
        return receiver_serializer.data

    class Meta:
        model = Reply
        exclude = ('create_at', 'delete_at')


class CommentSerializer(serializers.ModelSerializer):

    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('article', 'content', 'creator')


class CommentDetailSerializer(serializers.ModelSerializer):

    creator = UserDetailSerializer(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    reply_nums = serializers.SerializerMethodField(read_only=True)

    def get_is_like(self, obj):
        user = self.context['request'].user
        if not isinstance(user, User):
            return False
        like = Like.objects.filter(user=user, like_id=obj.id, like_type='comment').first()
        if not like:
            return False
        return like.id

    def get_reply_nums(self, obj):
        reply_nums = obj.replies.count()
        return reply_nums

    class Meta:
        model = Comment
        exclude = ('create_at', 'delete_at')


class MessageSerializer(serializers.ModelSerializer):

    content = serializers.CharField(label='留言内容')
    anonymous = serializers.BooleanField(label='匿名')
    creator = UserDetailSerializer(read_only=True)

    def get_creator(self, obj):
        if obj.anonymous:
            user = User.objects.filter(id=1).first()
        else:
            user = obj.user
        user_serializer = UserDetailSerializer(user, context={'request': self.context['request']})
        return user_serializer.data

    class Meta:
        model = Message
        fields = ('content', 'anonymous', 'creator')
