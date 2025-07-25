from django.db import models
from django.conf import settings


class BlogReaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    REACTION_CHOICES = (
    ('like', 'Like'), ('dislike', 'Dislike'),
    )

    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('user', 'blog_post')