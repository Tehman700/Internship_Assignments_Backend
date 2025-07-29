from django.db import models
from django.conf import settings

class BlogComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # Removed unique_together constraint to allow multiple comments per user per post

    def __str__(self):
        return f"{self.user.username} - {self.comment[:50]}..."

    @property
    def is_reply(self):
        return self.parent_comment is not None

    def get_replies(self):
        return self.replies.all().order_by('created_at')