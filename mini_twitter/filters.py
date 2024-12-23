from django_filters import rest_framework as filters

from mini_twitter.models import Post


class PostFilter(filters.FilterSet):
    author = filters.CharFilter(
        field_name='author__username',
        lookup_expr='icontains'
    )
    content = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['author', 'content']
