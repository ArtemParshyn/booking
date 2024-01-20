from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import UserSerializer, HotelSerializer, BookSerializer, RoomSerializer
from .models import ApiUser, Booking, Room, Hotel


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', "path", "get"]
    serializer_class = UserSerializer


class HotelModelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    http_method_names = ['post', "patсh", "get", "delete"]
    serializer_class = HotelSerializer


class RoomModelViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    http_method_names = ['post', "patсh", "get", "delete"]
    serializer_class = RoomSerializer


class BookingModelViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()



    serializer_class = BookSerializer
    def get(self, request):
        queryset = Room.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            print(validated_data)
            for i in Booking.objects.all().filter(room=validated_data["room"]):
                print(validated_data["start"], i.start, validated_data["end"])
                if (validated_data["start"] <= i.start <= validated_data["end"] or
                        validated_data["start"] <= i.end <= validated_data["end"]):
                    return Response("Already reserved", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

