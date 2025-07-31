from django.db import models
from django.conf import settings
from blogapp.Models.BlogComment import BlogComment


class BlogCommentReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} {self.reaction_type}d comment by {self.comment.user.username}"