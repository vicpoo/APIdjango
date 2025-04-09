from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'difficulties', views.DifficultyViewSet, basename='difficulty')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'cardpairs', views.CardPairViewSet, basename='cardpair')
router.register(r'games', views.GameViewSet, basename='game')
router.register(r'scores', views.ScoreViewSet, basename='score')
router.register(r'moves', views.MoveViewSet, basename='move')

urlpatterns = [
    path('', include(router.urls)),
    # Comenta o elimina la siguiente línea si no quieres usar coreapi
    # path('docs/', include_docs_urls(
    #     title='Memorama API',
    #     description='API documentation for Memorama Game',
    #     public=True
    # )),
]