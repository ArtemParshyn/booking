from django.db.models import Count
from rest_framework import serializers, validators

from . import models
from .models import ApiUser, Booking, Hotel, Room


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64, validators=[validators.UniqueValidator(ApiUser.objects.all())])
    email = serializers.EmailField(validators=[validators.UniqueValidator(ApiUser.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)
    reservations = serializers.JSONField()

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
            choice=validated_data["choice"]
        )
        user.set_password(validated_data["password"])
        user.save(update_fields=["password"])
        return user





class RoomSerializer(serializers.Serializer):

    number = serializers.IntegerField()
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    status = serializers.ChoiceField(choices=models.choices)

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
            status=validated_data["status"]
        )
        return room

class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = ["name", "street", "cost", "rooms"]

class BookSerializer(serializers.Serializer):
    class Meta:
        model = Booking
        fields = ["room", "start", "end"]

    def create(self, validated_data):
        ...
        # if validated_data["start"] > validated_data["end"]:
