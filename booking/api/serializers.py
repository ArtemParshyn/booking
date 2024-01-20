from django.db.models import Count
from rest_framework import serializers, validators

from . import models
from .models import ApiUser, Booking, Hotel, Room




class RoomSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())

    def validate(self, data):
        hotel = data['hotel']
        number = data['number']
        print(hotel, number)
        existing_room = Room.objects.filter(hotel=hotel, number=number).first()
        if existing_room:
            raise serializers.ValidationError("Комната с таким номером уже существует в этом отеле.")
        return data

    def create(self, validated_data):
        room = Room.objects.create(
            number=validated_data["number"],
            hotel=validated_data["hotel"],
        )
        return room


class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ["name", "street", "cost", "rooms"]


class BookSerializer(serializers.Serializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    start = serializers.DateField()
    end = serializers.DateField()
    user = serializers.PrimaryKeyRelatedField(queryset=ApiUser.objects.all())

    def validate(self, data):
        start = data["start"]
        end = data["end"]
        if start < end:
            return data
        else:
            raise serializers.ValidationError("Время заезда должно быть раньше чем выезд")

    def create(self, validated_data):
        booking = Booking.objects.create(
            room=validated_data["room"],
            start=validated_data["start"],
            end=validated_data["end"],
            user=validated_data["user"],
        )
        return booking


class UserSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=64, validators=[validators.UniqueValidator(ApiUser.objects.all())])
    email = serializers.EmailField(validators=[validators.UniqueValidator(ApiUser.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)
    rooms = BookSerializer(many=True, read_only=True)

    class Meta:
        model = ApiUser
        fields = ["username", "email", "password", "rooms"]

    def update(self, instance, validated_data):
        if email := validated_data.get("email"):
            instance.email = email
            instance.save(update_fields=["email"])
        if password := validated_data.get("password"):
            instance.set_password(password)
            instance.save(update_fields=["password"])
        return instance

    def create(self, validated_data):
        user = ApiUser.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user
