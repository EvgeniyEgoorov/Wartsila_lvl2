from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

