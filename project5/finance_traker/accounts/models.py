from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
# Create your models here.


class User(AbstractUser):


    def user_level(self):
        level = 'User'
        if self.is_superuser:
            level = 'Admin'
        return level

