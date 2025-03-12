from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PanierViewSet

router = DefaultRouter()
router.register(r'panier', PanierViewSet, basename='panier')

urlpatterns = [
    path('', include(router.urls)),
]
