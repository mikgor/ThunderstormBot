from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def UpdateUser(request):
    messengerId = request.GET.get('messengerid', None)
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)
    if messengerId is None or latitude is None or latitude is None:
        return HttpResponse("Empty field(s)")
    if not User.objects.filter(messengerId=messengerId).exists():
        User.objects.create(messengerId=messengerId, latitude=latitude, longitude=longitude)
    else:
        User.objects.get(messengerId=messengerId).UpdateLocation(latitude, longitude)
    for u in User.objects.all():
        print(u.messengerId)
        print(u.latitude)
        print(u.longitude)
    return HttpResponse("OK")
