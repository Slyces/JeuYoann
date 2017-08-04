from django.contrib import admin
from . import models

# Register your models here.
from . import models

admin.register(models.Player)
admin.register(models.Game)
admin.register(models.Tag)
admin.register(models.Activity)
