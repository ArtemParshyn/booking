from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, BookingModelViewSet, HotelModelViewSet, RoomModelViewSet
router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('hotel', HotelModelViewSet)
router.register('room', RoomModelViewSet)
router.register('booking', BookingModelViewSet)
urlpatterns = []
urlpatterns.extend(router.urls)