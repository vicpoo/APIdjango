#game/models.py
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('El email es obligatorio')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class Difficulty(models.Model):
    difficulty_id = models.AutoField(primary_key=True, db_column='difficulty_id')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    multiplier = models.FloatField(default=1.0)

    class Meta:
        db_table = 'difficulties'

    def __str__(self):
        return self.name

class Category(models.Model):
    category_id = models.AutoField(primary_key=True, db_column='category_id')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class CardPair(models.Model):
    class PairType(models.TextChoices):
        LETTER_IMAGE = 'letter-image', _('Letra con Imagen')
        WORD_DEFINITION = 'word-definition', _('Palabra con Definición')
        WORD_IMAGE = 'word-image', _('Palabra con Imagen')
        SYNONYM_ANTONYM = 'synonym-antonym', _('Sinónimo/Antónimo')

    pair_id = models.AutoField(primary_key=True, db_column='pair_id')
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.CASCADE,
        db_column='difficulty_id'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='category_id'
    )
    card_a = models.CharField(max_length=255)
    card_b = models.CharField(max_length=255)
    pair_type = models.CharField(max_length=20, choices=PairType.choices)

    class Meta:
        db_table = 'card_pairs'

    def __str__(self):
        return f"{self.card_a} - {self.card_b}"

class Game(models.Model):
    game_id = models.AutoField(primary_key=True, db_column='game_id')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.CASCADE,
        db_column='difficulty_id'
    )
    start_time = models.DateTimeField(auto_now_add=True, db_column='start_time')
    end_time = models.DateTimeField(null=True, blank=True, db_column='end_time')
    completed = models.BooleanField(default=False, db_column='completed')

    class Meta:
        db_table = 'games'

    def __str__(self):
        return f"Game {self.game_id} by {self.user.username}"

class Score(models.Model):
    score_id = models.AutoField(primary_key=True, db_column='score_id')
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        db_column='game_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )
    points = models.IntegerField(db_column='points')
    time_taken = models.IntegerField(db_column='time_taken')
    matches = models.IntegerField(db_column='matches')
    mismatches = models.IntegerField(db_column='mismatches')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'scores'

    def __str__(self):
        return f"{self.points} pts by {self.user.username}"

class Move(models.Model):
    move_id = models.AutoField(primary_key=True, db_column='move_id')
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        db_column='game_id'
    )
    card_a = models.ForeignKey(
        CardPair,
        on_delete=models.CASCADE,
        related_name='card_a_moves',
        db_column='card_a_id'
    )
    card_b = models.ForeignKey(
        CardPair,
        on_delete=models.CASCADE,
        related_name='card_b_moves',
        db_column='card_b_id'
    )
    is_match = models.BooleanField(db_column='is_match')
    move_time = models.DateTimeField(auto_now_add=True, db_column='move_time')

    class Meta:
        db_table = 'moves'

    def __str__(self):
        return f"Move {self.move_id} in Game {self.game_id}"