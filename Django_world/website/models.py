from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# =============================================================================
class Game(models.Model):
    pass


# =============================================================================
genders = (
    ('H', 'Homme'),
    ('F', 'Femme'),
    ('N', 'Neutre'),
)


class Player(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=genders)

    class Meta:
        unique_together = ('game', 'name',)


# =============================================================================
class Tag(models.Model):
    name = models.CharField(max_length=50)


# =============================================================================
class Activity(models.Model):
    text = models.TextField()
    tags = models.ForeignKey(Tag)
