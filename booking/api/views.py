from rest_framework import viewsets
from api.serializers import UserSerializer, HotelSerializer, BookSerializer, RoomSerializer
from .models import ApiUser, Booking, Room, Hotel


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', "path", "get"]
    serializer_class = UserSerializer


class HotelModelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    http_method_names = ['post', "path", "get", "delete"]
    serializer_class = HotelSerializer


class RoomModelViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    http_method_names = ['post', "path", "get", "delete"]
    serializer_class = RoomSerializer


class BookingModelViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    http_method_names = ['post', "path", "get", "delete"]
    serializer_class = BookSerializer

