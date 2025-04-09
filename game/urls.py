# game/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, DifficultyViewSet, CategoryViewSet,
    CardPairViewSet, GameViewSet, ScoreViewSet, MoveViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'difficulties', DifficultyViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'cardpairs', CardPairViewSet)
router.register(r'games', GameViewSet)
router.register(r'scores', ScoreViewSet)
router.register(r'moves', MoveViewSet)

urlpatterns = [
    path('', include(router.urls)),
]