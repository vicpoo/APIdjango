# game/serializers.py
from rest_framework import serializers
from .models import User, Difficulty, Category, CardPair, Game, Score, Move

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    password = serializers.CharField(write_only=True)  # Campo añadido

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password', 'created_at', 'last_login']
        extra_kwargs = {
            'last_login': {'format': '%Y-%m-%d %H:%M:%S'}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class DifficultySerializer(serializers.ModelSerializer):
    difficulty_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Difficulty
        fields = ['difficulty_id', 'name', 'description', 'multiplier']

class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Category
        fields = ['category_id', 'name', 'description']

class CardPairSerializer(serializers.ModelSerializer):
    pair_id = serializers.IntegerField(source='id', read_only=True)
    pair_type = serializers.ChoiceField(
        choices=CardPair.PairType.choices,
        error_messages={'invalid_choice': 'Tipo de par no válido'}
    )

    class Meta:
        model = CardPair
        fields = ['pair_id', 'difficulty', 'category', 'card_a', 'card_b', 'pair_type']

class GameSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(source='id', read_only=True)
    user = UserSerializer(read_only=True)
    difficulty = DifficultySerializer(read_only=True)
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        allow_null=True
    )

    class Meta:
        model = Game
        fields = ['game_id', 'user', 'difficulty', 'start_time', 'end_time', 'completed']

class ScoreSerializer(serializers.ModelSerializer):
    score_id = serializers.IntegerField(source='id', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Score
        fields = ['score_id', 'game', 'user', 'points', 'time_taken', 
                 'matches', 'mismatches', 'created_at']

class MoveSerializer(serializers.ModelSerializer):
    move_id = serializers.IntegerField(source='id', read_only=True)
    move_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Move
        fields = ['move_id', 'game', 'card_a', 'card_b', 'is_match', 'move_time']