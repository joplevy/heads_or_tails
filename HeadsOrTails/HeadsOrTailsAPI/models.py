from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    address = models.TextField(default='0x0')
    title = models.TextField(default='Game title')
    head = models.BooleanField(default=False)
    value = models.IntegerField()
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)