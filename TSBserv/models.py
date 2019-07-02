from django.db import models

class User(models.Model):
    messengerId = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    active = models.BooleanField(default=True)

    def UpdateLocation(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.save()
