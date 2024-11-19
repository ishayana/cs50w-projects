from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE , related_name='posts')
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"

    def like_count(self):
        return self.likes.all().count()
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userliked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} followed {self.following}'
