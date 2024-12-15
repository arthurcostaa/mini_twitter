from django.contrib import admin

from mini_twitter.models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ['content', 'author']
    list_display = ['id', 'author', 'content', 'created_at', 'updated_at']
    list_display_links = ['id', 'content']
    list_filter = ['author']
    search_fields = ['content']
    list_per_page = 20

admin.site.register(Post, PostAdmin)
