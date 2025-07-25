from django.contrib.auth.models import AbstractUser
from django.db import models


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







