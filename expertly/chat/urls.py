from django.urls import path
from .views import ChatViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ChatViewSet)  # Register the ChatViewSet

urlpatterns = router.urls