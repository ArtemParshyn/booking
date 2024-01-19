from django.contrib.auth.models import AbstractUser
from django.db import models

choices = [
    ("F", "free"),
    ("R", "reserved")
]


class User(AbstractUser):
    ...


class Hotel(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    cost = models.IntegerField()
    status = models.CharField(choices=choices)


class Booking(models.Model):
    name = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
