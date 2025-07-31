from django.db import models
from django.conf import settings

# This is the model for blogpost that contains the title, and content which users will write in JSON rest will be automatically fetchedd
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
