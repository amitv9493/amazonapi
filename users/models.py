from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    amazon_authorization = models.BooleanField(default=False)
    
    
