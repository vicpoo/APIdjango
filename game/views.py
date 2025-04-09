# game/views.py
from rest_framework import viewsets
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
    
    def get_queryset(self):
        queryset = CardPair.objects.select_related('difficulty', 'category')
        difficulty = self.request.query_params.get('difficulty')
        category = self.request.query_params.get('category')
        
        if difficulty:
            queryset = queryset.filter(difficulty_id=difficulty)
        if category:
            queryset = queryset.filter(category_id=category)
            
        return queryset

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    lookup_field = 'game_id'
    queryset = Game.objects.select_related('user', 'difficulty').prefetch_related(
        'score_set', 'move_set'
    ).order_by('-start_time')

class ScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    lookup_field = 'score_id'
    
    def get_queryset(self):
        queryset = Score.objects.select_related('user', 'game')
        user = self.request.query_params.get('user')
        
        if user:
            queryset = queryset.filter(user_id=user)
            
        return queryset.order_by('-points')

class MoveViewSet(viewsets.ModelViewSet):
    serializer_class = MoveSerializer
    lookup_field = 'move_id'
    
    def get_queryset(self):
        game = self.request.query_params.get('game')
        if game:
            return Move.objects.filter(game_id=game).select_related('card_a', 'card_b')
        return Move.objects.all().select_related('card_a', 'card_b')