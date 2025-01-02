from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    content = models.TextField(max_length=280, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_comments(self) -> int:
        return self.comments.count()

    @property
    def total_likes(self) -> int:
        return self.likes.count()

    def __str__(self):
        return f'{self.id} - {self.content[:30]}'

    class Meta:
        ordering = ['-created_at', 'author']


class Comment(models.Model):
    comment = models.TextField(max_length=280, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.comment[:30]}'

    class Meta:
        ordering = ['-created_at', 'author']
