from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter, CharFilter

from content.models import Article


class ArticleFilter(FilterSet):
    """
    文章的过滤器
    """
    tag = CharFilter(field_name='tags', lookup_expr='icontains')
    search = CharFilter(field_name='title', lookup_expr='icontains')
    category = NumberFilter(field_name='category', lookup_expr='exact')
    time = CharFilter(method='time_filter')

    def time_filter(self, queryset, name, value):
        year, month = value.split('-')
        queryset = queryset.filter(create_at__year=year).filter(create_at__month=month)
        return queryset

    class Meta:
        model = Article
        fields = ['category', 'time', 'search', 'tag']
