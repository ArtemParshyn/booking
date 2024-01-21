from django.contrib.auth.models import AbstractUser
from django.db import models


class ApiUser(AbstractUser):
    ...


class Hotel(models.Model):
    name = models.CharField(max_length=64, unique=True)
    street = models.CharField(max_length=64)
    cost = models.IntegerField()


class Room(models.Model):
    number = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    user = models.ForeignKey(ApiUser, on_delete=models.CASCADE)
