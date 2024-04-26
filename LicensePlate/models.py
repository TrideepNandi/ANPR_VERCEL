from django.db import models

# Create your models here.

from django.conf import settings

class LicensePlate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_plate_text = models.CharField(max_length=255)

class Record(models.Model):
    license_plate = models.ForeignKey(LicensePlate, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    # image = models.ImageField()