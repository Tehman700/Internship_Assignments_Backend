from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings




# Below is the Model for Users that contain all the necessary fields for Registering the User
class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    ROLE_CHOICES = (
        ('writer', 'Writer'),                           # Role choices are used so that we can change permissions accordingly
        ('viewer', 'Viewer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    REQUIRED_FIELDS = ['email', 'mobile_number', 'role', 'first_name', 'last_name']          # These are the rest fields required







# THis is the model for blogpost that contains the title, and content which users will write in JSON rest will be automatically fetched

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title