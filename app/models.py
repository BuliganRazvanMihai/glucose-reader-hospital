from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Device (models.Model):
    patientId = models.IntegerField(unique=False)
    deviceId = models.IntegerField(unique=True)
    hour = models.DateTimeField()
    type = models.IntegerField()
    glucoseValue = models.IntegerField()