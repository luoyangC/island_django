from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from api.core.views import send_sms_code, get_token, tulin_talk, get_upload_token
from api.user.views import get_user_info
from api.content.views import get_article_archives, get_article_profiles, get_article_tags
from api.user import views as user_views
from api.content import views as content_views
from api.action import views as action_views

router = DefaultRouter()

router.register('users', user_views.UserViewSet, basename='users')

router.register('sentences', content_views.SentenceViewSet, basename='sentences')

router.register('categories', content_views.CategoryViewSet, basename='categories')

router.register('likes', action_views.LikeViewSet, basename='likes')

router.register('faves', action_views.FavViewSet, basename='faves')

router.register('comments', action_views.CommentViewSet, basename='comments')

router.register('replies', action_views.ReplyViewSet, basename='replies')

router.register('messages', action_views.MessageViewSet, basename='messages')

router.register('articles', content_views.ArticleViewSet, basename='articles')

urlpatterns = [
    # 后台管理
    path('admin/', admin.site.urls),
    # 获取授权
    path('api/<str:version>/core/token/', get_token),
    # 发送短信验证码
    path('api/<str:version>/core/code/', send_sms_code),
    # 图灵机器人接口
    path('api/<str:version>/core/talk/', tulin_talk),
    # 获取文件上传token
    path('api/<str:version>/core/upload/', get_upload_token),

    path('api/<str:version>/users/info/', get_user_info),

    path('api/<str:version>/articles/tags/', get_article_tags),

    path('api/<str:version>/articles/profiles', get_article_profiles),
    
    path('api/<str:version>/articles/archives', get_article_archives),

    # API入口
    path('api/<str:version>/', include(router.urls)),
]


