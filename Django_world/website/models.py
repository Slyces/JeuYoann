from django.db import models
from random import choice

# =============================================================================
from django.db.models import Count


class Game(models.Model):
    pass


# =============================================================================
genders = (
    ('H', 'Garçon'),
    ('F', 'Fille'),
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
    tags = models.ManyToManyField(Tag)

    @staticmethod
    def random(tag_list=None):
        print(Activity.objects.all())
        return choice(Activity.objects.all())
