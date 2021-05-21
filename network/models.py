from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return f"{self.user}, {self.text}, {self.created_at}, {self.likes} likes"


class Followers(models.Model):
    whom = models.ForeignKey(User, related_name="whom", on_delete=models.CASCADE)
    who = models.ForeignKey(User, related_name="who", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.who} follows {self.whom}"

    objects = models.Manager()
