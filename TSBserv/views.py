from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from TSB.local_settings import *
from .classes.weatherApiHandler import WeatherApiHandler
from .classes.messengerApiHandler import MessengerApiHandler
from .classes.city import City
import requests

def SendNotifications(request):
    ip = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip not in ALLOWED_API_REQUEST_IP:
        return HttpResponse("Access denied")
    for user in User.objects.all():
        apiRequest = WeatherApiHandler().Request("lat="+str(user.latitude)+"&lon="+str(user.longitude))
        mainCity = City(apiRequest["list"][0])
        distance = 50
        stormFound = False
        for city in apiRequest["list"]:
            currentCity = City(city)
            if currentCity.Storm:
                currentDist = currentCity.Calculate(mainCity.Lat, mainCity.Lon)['distance']
                if currentDist < distance and currentDist > 0:
                    distance = currentDist
                    stormFound = True
        if stormFound:
            print(distance)
        MessengerApiHandler().SendResponseMessage(user.messengerId, mainCity.Name)
    return HttpResponse("OK")

def IncomingMessage(request):
    ip = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip not in ALLOWED_API_REQUEST_IP:
        return HttpResponse("Access denied")
    messageType = int(request.GET.get('messagetype', None)) #1- getstarted 2-location 3-other
    messengerId = request.GET.get('messengerid', None)
    if messageType is None or messengerId is None:
        return HttpResponse("Empty field(s)")
    if messageType == 1:
        r = MessengerApiHandler().SendResponseMessage(messengerId, "Welcome. You have been registered. Send your location to get started.")
    if messageType == 2:
        latitude = request.GET.get('latitude', None)
        longitude = request.GET.get('longitude', None)
        if latitude is None or latitude is None:
            return HttpResponse("Empty field(s)")
        if not User.objects.filter(messengerId=messengerId).exists():
            User.objects.create(messengerId=messengerId, latitude=latitude, longitude=longitude)
        else:
            User.objects.get(messengerId=messengerId).UpdateLocation(latitude, longitude)
        r = MessengerApiHandler().SendResponseMessage(messengerId, "Location received. Thank you :).")
    if messageType == 3:
        text = request.GET.get('text', None)
        if text is None:
            return HttpResponse("Empty field(s)")
        r = MessengerApiHandler().SendAutoResponseMessage(messengerId, text)
    return HttpResponse("OK")
