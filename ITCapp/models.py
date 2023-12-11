from django.db import models


# Create your models here.
class person(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class AppUser(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
