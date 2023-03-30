from django.db import models

# Create your models here.
class VillagerResponseDB(models.Model):
    villager_option = models.TextField()
    villager_why = models.TextField()