from django.db import models
from django.conf import settings

class BlogComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog_post = models.ForeignKey('Models.BlogPost', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'blog_post')
