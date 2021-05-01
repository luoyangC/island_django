from django.contrib import admin

# Register your models here.

from content.models import Sentence, Category, Article


class SentenceAdmin(admin.ModelAdmin):
    fields = ['lines']
    search_fields = ['id', 'lines']
    list_display = ['id', 'lines', 'create_at', 'update_at']


class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'info']
    search_fields = ['id', 'title']
    list_display = ['id', 'title', 'create_at', 'update_at']


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'tags', 'profile',
              'image', 'content', 'creator', 'category']
    search_fields = ['id', 'title']
    list_display = ['id', 'title', 'creator',
                    'category', 'create_at', 'update_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Sentence, SentenceAdmin)
