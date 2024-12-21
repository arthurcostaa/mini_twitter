from django.contrib import admin

from mini_twitter.models import Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    fields = ['content', 'author']
    list_display = [
        'id',
        'author',
        'content',
        'total_comments',
        'created_at',
        'updated_at',
    ]
    list_display_links = ['id', 'content']
    list_filter = ['author']
    search_fields = ['content']
    list_per_page = 20
    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    fields = ['comment', 'author', 'post']
    list_display = ['id', 'author', 'comment', 'post', 'created_at', 'updated_at']
    list_display_links = ['id', 'comment']
    list_filter = ['author', 'post']
    search_fields = ['comment']
    list_per_page = 20


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
