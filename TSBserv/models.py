from django.db import models
from django.utils import timezone
from django.db.models.signals import post_init

class UserStormEvent(models.Model):
    active = models.BooleanField(default=False)
    updatedAt = models.DateTimeField(default=timezone.now, null=True)
    distance = models.FloatField(default=0)
    latitudeDirection = models.CharField(max_length=1)
    lontitudeDirection = models.CharField(max_length=1)

    def UpdateDetails(self, details):
        self.distance = details['distance']
        self.latitudeDirection = details['latDirection']
        self.lonDirection = details['lonDirection']
        self.lastStormEvent = timezone.now()
        self.save()

    def SetStatus(self):
        self.active = not self.active
        self.save()

    def IsUpdated(self, details):
        if self.distance == details['distance'] or self.latitudeDirection == details['latDirection'] or self.lonDirection == details['lonDirection']:
            return False
        return True

class User(models.Model):
    messengerId = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    active = models.BooleanField(default=True)
    dateJoined = models.DateTimeField(default=timezone.now, null=True)
    stormEvent = models.OneToOneField(UserStormEvent, on_delete=models.CASCADE)

    def UpdateLocation(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.save()

def UserAddUserStormEventObject(**kwargs):
   instance = kwargs.get('instance')
   instance.stormEvent = UserStormEvent.objects.create()

post_init.connect(UserAddUserStormEventObject, User)
