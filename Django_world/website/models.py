from django.db import models
from django.contrib.auth.models import User
from random import choice
from datetime import datetime
from django.db.models import Count
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


# =============================================================================
# Penser au select related en cas de foreign key
# ------ -- prefetch related ------- many to many fields
# =============================================================================


# =============================================================================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creation_date = models.DateField(default=datetime.now())
    decks = models.ManyToManyField(Deck)
    cards = models.ManyToManyField(Card)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# =============================================================================
genders = (
    ('H', 'Garçon'),
    ('F', 'Fille'),
)


# =============================================================================
class Player(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=genders)

    class Meta:
        unique_together = ('game', 'name',)


# =============================================================================
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


# =============================================================================
class Card(models.Model):
    title = models.CharField(max_length=50, null=True)
    text = models.TextField()
    author = models.ForeignKey(User)
    categories = models.ManyToManyField(Category)
    played = models.IntegerField(default=0)
    passed = models.IntegerField(default=0)

    def get_absolute_url(self):
        return 'cards/{card_id}/'.format(card_id=self.id)


# =============================================================================
class Deck(models.Model):
    name = models.CharField(max_length=50)
    cards = models.ManyToManyField(Card)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._size = 0

    class Meta:
        unique_together = ('name', 'author',)

    def add_card(self, card):
        Membership.objects.create(deck=self, card=card)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def get_absolute_url(self):
        return 'decks/{deck_id}'.format(deck_id=self.id)


@receiver(m2m_changed, sender=Deck, dispatch_uid="update_stock_count")
def update_size(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    if action == 'post_add':
        instance.size = instance.cards.all().count()


# =============================================================================
class Membership(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date_added = models.DateField(default=datetime.now())


# =============================================================================
class PlayCards(models.Model):
    card = models.ForeignKey(Card)
    played = models.BooleanField(default=False)


# =============================================================================
exploration_algorithms = (
    ('S', 'Tirage aléatoire sans remise'),
    ('R', 'Tirage aléatoire avec remise'),
    ('O', 'Tirage ordonné'),
)


class Game(models.Model):
    password = models.CharField(max_length=50)
    deck = models.ForeignKey(Deck)
    algorithm = models.CharField(choices=exploration_algorithms, default='S')
    cards = models.ManyToManyField(PlayCards)


@receiver(post_save, sender=Game)
def save_game(sender, instance, **kwargs):
    pass
