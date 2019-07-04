from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from TSB.local_settings import *
from .classes.weatherApiHandler import WeatherApiHandler
from .classes.messengerApiHandler import MessengerApiHandler
from .classes.city import City
import requests
from django.utils import timezone
import datetime
import json
from django.views.decorators.csrf import csrf_exempt

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
        print(user.stormEvent.active)
        print(user.stormEvent.updatedAt)
        print(user.stormEvent.distance)
        print(user.stormEvent.latitudeDirection)
        print(user.stormEvent.lontitudeDirection)
        print(user.dateJoined)
        if user.stormEvent.active and (timezone.now()-user.stormEvent.updatedAt).seconds < 300:
            continue
        apiRequest = WeatherApiHandler().Request("lat="+str(user.latitude)+"&lon="+str(user.longitude))
        mainCity = City(apiRequest["list"][0])
        distance = 50
        stormFound = False
        stormDetails = ""
        for city in apiRequest["list"]:
            currentCity = City(city)
            if currentCity.Storm:
                stormDetails = currentCity.Calculate(mainCity.Lat, mainCity.Lon)
                if stormDetails['distance'] < distance and stormDetails['distance'] > 0:
                    distance = stormDetails['distance']
                    stormFound = True
        if stormFound:
            if not user.stormEvent.active:
                user.stormEvent.SetStatus()
            if user.stormEvent.IsUpdated(stormDetails):
                MessengerApiHandler().SendResponseMessage(user.messengerId, "Wykryto burze " + str(round(distance, 1)) +" kilometrów od " + mainCity.Name + ". Kierunek: " + stormDetails['latDirection']+ stormDetails['lonDirection'])
            user.stormEvent.UpdateDetails(stormDetails)
        else:
            if user.stormEvent.active:
                user.stormEvent.SetStatus()
    return HttpResponse("OK")

@csrf_exempt
def IncomingMessage(request):
    ip = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip not in ALLOWED_API_REQUEST_IP:
        return HttpResponse("Access denied")
    data = json.loads(request.body.decode("utf-8"))
    messaging = data['entry'][0]['messaging'][0]
    print(data)
    messengerId = messaging['sender']['id']
    messageAttachments = ''
    messageAttachmentsType = ''
    postbackPayload = ''
    if 'message' in messaging:
        if 'text' in messaging['message']:
            messageAttachments = 'text'
        else:
            messageAttachments = messaging['message']['attachments'][0]
            messageAttachmentsType = messaging['message']['attachments'][0]['type']
    if not messageAttachments:
        postbackPayload = messaging['postback']['payload']
    if messageAttachments and messageAttachmentsType == "location":
        latitude = messageAttachments['payload']['coordinates']['lat']
        longitude = messageAttachments['payload']['coordinates']['long']
        if not User.objects.filter(messengerId=messengerId).exists():
            user = User.objects.create(messengerId=messengerId, latitude=latitude, longitude=longitude, stormEvent = UserStormEvent.objects.create())
        else:
            User.objects.get(messengerId=messengerId).UpdateLocation(latitude, longitude)
        r = MessengerApiHandler().SendResponseMessage(messengerId, "Location received. Thank you :).")
    elif postbackPayload and postbackPayload == "GET_STARTED_PAYLOAD":
        r = MessengerApiHandler().SendResponseMessage(messengerId, "Welcome. Send your location to sign up.")
    else:
        text = ''
        if not messageAttachments:
            text = messaging['message']['text']
        r = MessengerApiHandler().SendAutoResponseMessage(messengerId, text.lower())
    return HttpResponse("OK")
