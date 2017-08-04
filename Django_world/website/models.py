from django.db import models
from random import randint

# =============================================================================
from django.db.models import Count


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
    tags = models.ManyToManyField(Tag)

    @staticmethod
    def random():
        count = Activity.objects.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return Activity.objects.all()[random_index]
