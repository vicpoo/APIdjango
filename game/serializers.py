# game/serializers.py
from rest_framework import serializers
from .models import User, Difficulty, Category, CardPair, Game, Score, Move

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    last_login = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'created_at', 'last_login']

class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CardPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardPair
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ['game_id', 'start_time', 'end_time', 'completed']

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = '__all__'