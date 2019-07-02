import json
import math

class City:
    Data = ''
    Name = ''
    Lon = 0.0
    Lat = 0.0
    Storm = False

    def __init__(self, data):
        self.Data = data
        self.Name = data["name"]
        self.Lon = float(data["coord"]["lon"])
        self.Lat = float(data["coord"]["lat"])
        for weather in data["weather"]:
            if int(weather["id"]) >= 200 and int(weather["id"]) <= 232:
                self.Storm = True
                break

    def Calculate(self, cityLat, cityLon):
        result = dict()
        latDistance = self.Lat-cityLat
        result['latDistance'] = latDistance
        lonDistance = self.Lon-cityLon
        result['lonDistance'] = lonDistance
        distance = math.sqrt(pow(latDistance,2) + pow(math.cos(cityLat*math.pi/180) * (lonDistance),2)) * 40075.704/360
        result['distance'] = distance
        lonDirection = 'W'
        latDirection = 'N'
        if distance > 0:
            if lonDistance > 0:
                lonDirection = 'E'
            if latDistance < 0:
                latDirection = 'S'
            if lonDistance == 0:
                lonDirection = ''
            if latDistance == 0:
                latDirection = ''
        result['latDirection'] = latDirection
        result['lonDirection'] = lonDirection
        return result
