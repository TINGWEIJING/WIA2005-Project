import requests
import json
import os
import sys

class TravelInfo:
    API_KEY = ""
    JsonRes = ""
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.req_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&alternatives=true&key={}'.format(origin,destination,self.API_KEY)
        self.JsonRes = requests.get(self.req_url).json()
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


class TravelInfoTEST:
    def __init__(self):
        self.getDirectionsAPI()
    
    def getDirectionsAPI(self):
        f = open(os.getcwd()+'/core/algorithm/sample.json')
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

     

if __name__ == "__main__":
    # a = TravelInfo("3.0319924887507144, 101.37344116244806","3.3615395462207878, 101.56318183511695")
    a = TravelInfoTEST()
    print(a.getShortestDistance())
    print(a.getShortestSteps())
