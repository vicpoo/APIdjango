# game/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class Difficulty(models.Model):
    difficulty_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    multiplier = models.FloatField(default=1.0)
    board_rows = models.PositiveSmallIntegerField(default=4)
    board_cols = models.PositiveSmallIntegerField(default=4)

    class Meta:
        db_table = 'difficulties'
        verbose_name_plural = 'difficulties'

    def __str__(self):
        return self.name

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class CardPair(models.Model):
    class PairType(models.TextChoices):
        LETTER_IMAGE = 'letter-image', _('Letra con Imagen')
        WORD_DEFINITION = 'word-definition', _('Palabra con Definición')
        WORD_IMAGE = 'word-image', _('Palabra con Imagen')
        SYNONYM_ANTONYM = 'synonym-antonym', _('Sinónimo/Antónimo')

    pair_id = models.AutoField(primary_key=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    card_a = models.CharField(max_length=255)
    card_b = models.CharField(max_length=255)
    pair_type = models.CharField(max_length=20, choices=PairType.choices)

    class Meta:
        db_table = 'card_pairs'
        unique_together = ('card_a', 'card_b', 'category')

    def __str__(self):
        return f"{self.card_a} - {self.card_b}"

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'games'

    def __str__(self):
        return f"Game {self.game_id} by {self.user.username}"

class Score(models.Model):
    score_id = models.AutoField(primary_key=True)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    time_taken = models.IntegerField()
    matches = models.IntegerField()
    mismatches = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'scores'

    def __str__(self):
        return f"{self.points} pts by {self.user.username}"

class Move(models.Model):
    move_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    card_a = models.ForeignKey(CardPair, on_delete=models.CASCADE, related_name='card_a_moves')
    card_b = models.ForeignKey(CardPair, on_delete=models.CASCADE, related_name='card_b_moves')
    is_match = models.BooleanField()
    move_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'moves'

    def __str__(self):
        return f"Move {self.move_id} in Game {self.game_id}"