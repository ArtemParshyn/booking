from rest_framework import serializers, validators
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


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["name", "street", "cost"]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('number', 'hotel', 'status')


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Booking
        fields = ["room", "start", "end"]

    def create(self, validated_data):
        ...
        # if validated_data["start"] > validated_data["end"]:
