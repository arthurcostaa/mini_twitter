from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    content = models.TextField(max_length=280, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:30]

    class Meta:
        ordering = ['-created_at', 'author']


class Comment(models.Model):
    comment = models.TextField(max_length=280, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:30]

    class Meta:
        ordering = ['-created_at', 'author']
