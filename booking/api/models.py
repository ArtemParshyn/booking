from django.contrib.auth.models import AbstractUser
from django.db import models

choices = [
    ("F", "free"),
    ("R", "reserved")
]


class ApiUser(AbstractUser):
    ...


class Hotel(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    cost = models.IntegerField()


class Room(models.Model):
    number = models.IntegerField(unique=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    status = models.CharField(max_length=1, choices=choices)


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    start = models.DateField()
    end = models.DateField()
