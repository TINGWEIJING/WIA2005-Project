import requests
import json
import os
import sys

class TravelInfo:
    JsonRes = ""
    def __init__(self, origin, destination):
        self.origin = origin
        # assume the waypoint delivery hub as port klang to ease the development
        self.destination = destination
        self.waypoint = "Kawasan Perusahaan Bandar Sultan Suleiman, 42000 Port Klang, Selangor"
        self.req_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoint}&key={API_KEY}'.format(origin = origin,destination = destination, waypoint = self.waypoint, API_KEY = self.API_KEY)
        # self.req_url = 'https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood&key=AIzaSyDUUCnl-iYsjapMKK-IyplHJrWHbPM12iI'
        content = json.dumps(requests.get(self.req_url).json())
        f = open("sample2.json", "w")
        f.write(content)
        f.close()
        self.JsonRes = content

    def getShortestRoute(self):
        self.shortestDistance = sys.maxsize
        print(self.JsonRes)
        for route in self.JsonRes['routes']:
            # calculate total distance of each route by adding all legs of the route
            total = 0
            for leg in self.JsonRes['routes']['legs']:
                total += leg['distance']['text']
            if total < self.shortestDistance:
                self.shortestRoute = route
                self.shortestDistance = total
        return self.shortestRoute

    def getShortestDistance(self):
        return self.shortestDistance
    
class TravelInfoTEST:
    def __init__(self):
        self.getDirectionsAPI()
    
    def getDirectionsAPI(self):
        f = open(os.getcwd()+'\\sample.json')
        self.JsonRes = json.loads(f.read())
        self.getShortestRoute()

    def getShortestRoute(self):
        shortestDistance = sys.maxsize
        for route in self.JsonRes['routes']:
            if(route['legs'][0]['distance']['value']<shortestDistance):
                self.shortestRoute = route['legs'][0]
                shortestDistance = route['legs'][0]['distance']['value']

    def getShortestDistance(self):
        return self.shortestRoute['distance']['text']

    def getShortestSteps(self):
        return self.shortestRoute['steps']

class TravelInfoUsingDistanceMatrix:
    def __init__(self):
        self.getDirectionsAPI()
    
    def getDirectionsAPI(self):
        f = open(os.getcwd()+'\\sample.json')
        self.JsonRes = json.loads(f.read())
        self.getShortestRoute()

    def getShortestRoute(self):
        shortestDistance = sys.maxsize
        for route in self.JsonRes['routes']:
            if(route['legs'][0]['distance']['value']<shortestDistance):
                self.shortestRoute = route['legs'][0]
                shortestDistance = route['legs'][0]['distance']['value']

    def getShortestDistance(self):
        return self.shortestRoute['distance']['text']

    def getShortestSteps(self):
        return self.shortestRoute['steps']
     
# origin - rawang
# 9-1, Jalan Mawar 4, Taman Kosaso, 48200 Serendah, Selangor

# destination - bukit jelutong
# 2, Jalan Kubah U8/58, Bukit Jelutong, 40150 Shah Alam, Selangor
if __name__ == "__main__":
    # a = TravelInfo("3.0319924887507144, 101.37344116244806","3.3615395462207878, 101.56318183511695")
    origin = "9-1, Jalan Mawar 4, Taman Kosaso, 48200 Serendah, Selangor"
    destination = "2, Jalan Kubah U8/58, Bukit Jelutong, 40150 Shah Alam, Selangor"
    a = TravelInfo(origin, destination)
    print(a.getShortestRoute())
