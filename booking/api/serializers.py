from rest_framework import serializers, validators
from .models import ApiUser, Booking, Hotel, Room


# serializers.py
class RoomSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    hotel = serializers.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(RoomSerializer, self).__init__(*args, **kwargs)
        self.fields['hotel'].choices = [f"{r.name}" for r in Hotel.objects.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['hotel'] = instance.hotel.name
        return representation

    def validate(self, data):
        hotel_name = data['hotel']
        number = data['number']
        existing_room = Room.objects.filter(hotel__name=hotel_name, number=number).first()
        if existing_room:
            raise serializers.ValidationError("Комната с таким номером уже существует в этом отеле.")
        return data

    def create(self, validated_data):
        hotel_name = validated_data["hotel"]
        hotel = Hotel.objects.get(name=hotel_name)
        room = Room.objects.create(
            number=validated_data["number"],
            hotel=hotel,
        )
        return room


class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ["name", "street", "cost", "rooms"]


class BookSerializer(serializers.Serializer):
    room = serializers.ChoiceField(choices=[])
    start = serializers.DateField()
    end = serializers.DateField()
    hotel = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(BookSerializer, self).__init__(*args, **kwargs)
        self.number = None
        self.hotel = None
        self.fields['room'].choices = [f"{r.hotel.name} {r.number}" for r in Room.objects.all()]
        # self.fields['user'].choices = [f"{r.username}" for r in ApiUser.objects.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['room'] = instance.room.number
        representation['hotel'] = instance.room.hotel.name
        representation["user"] = instance.user.username
        return representation

    def validate(self, data):
        start = data["start"]
        end = data["end"]
        self.hotel = data["room"].split(" ")[0]
        self.number = int(data["room"].split(" ")[1]),
        self.number = self.number[0]
        data["hotel"] = Hotel.objects.get(name=self.hotel)
        data["room"] = Room.objects.get(number=self.number, hotel=data["hotel"])
        if start < end:
            return data
        else:
            raise serializers.ValidationError("Время заезда должно быть раньше чем выезд")

    def create(self, validated_data):
        print(f"validated data in seriaz = {validated_data}")

        booking = Booking.objects.create(
            room=validated_data["room"],
            start=validated_data["start"],
            end=validated_data["end"],
            user=validated_data["user"],
            hotel=validated_data["hotel"],
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
