#game/view.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.utils import timezone
from .models import User, Difficulty, Category, CardPair, Game, Score, Move
from .serializers import (
    UserSerializer, DifficultySerializer, CategorySerializer,
    CardPairSerializer, GameSerializer, ScoreSerializer, MoveSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    lookup_field = 'user_id'

class DifficultyViewSet(viewsets.ModelViewSet):
    queryset = Difficulty.objects.all().order_by('multiplier')
    serializer_class = DifficultySerializer
    lookup_field = 'difficulty_id'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    lookup_field = 'category_id'

class CardPairViewSet(viewsets.ModelViewSet):
    serializer_class = CardPairSerializer
    lookup_field = 'pair_id'
    queryset = CardPair.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('difficulty', 'category')
        difficulty = self.request.query_params.get('difficulty')
        category = self.request.query_params.get('category')
        
        if difficulty and category:
            try:
                queryset = queryset.filter(
                    difficulty_id=int(difficulty),
                    category_id=int(category)
                )
            except (ValueError, TypeError):
                pass
        return queryset

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    lookup_field = 'game_id'
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('user', 'difficulty', 'category')
        user = self.request.query_params.get('user')
        
        if user:
            try:
                queryset = queryset.filter(user_id=int(user))
            except (ValueError, TypeError):
                pass
        return queryset.order_by('-start_time')
    
    @action(detail=True, methods=['patch'])
    def complete(self, request, game_id=None):
        game = self.get_object()
        game.completed = True
        game.end_time = timezone.now()
        game.save()
        return Response({'status': 'game completed'})

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    lookup_field = 'score_id'
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('user', 'game')
        user = self.request.query_params.get('user')
        
        if user:
            try:
                queryset = queryset.filter(user_id=int(user))
            except (ValueError, TypeError):
                pass
        return queryset.order_by('-points')

class MoveViewSet(viewsets.ModelViewSet):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer
    lookup_field = 'move_id'
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('game', 'card_a', 'card_b')
        game = self.request.query_params.get('game')
        
        if game:
            try:
                queryset = queryset.filter(game_id=int(game))
            except (ValueError, TypeError):
                pass
        return queryset.order_by('move_time')