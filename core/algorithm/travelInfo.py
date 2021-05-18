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
        self.req_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoint}&key={API_KEY}'.format(
            origin=origin, destination=destination, waypoint=self.waypoint, API_KEY=self.API_KEY)
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
            if(route['legs'][0]['distance']['value'] < shortestDistance):
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
            if(route['legs'][0]['distance']['value'] < shortestDistance):
                self.shortestRoute = route['legs'][0]
                shortestDistance = route['legs'][0]['distance']['value']

    def getShortestDistance(self):
        return self.shortestRoute['distance']['text']

    def getShortestSteps(self):
        return self.shortestRoute['steps']

# OpenRouteService api requires longlat but not latlong
class HubRouting:

    HUB_LOCATION_JSON_FILE = os.getcwd()+'\\core\\storage\\hub_location.json'
    HUB_LOCATION = {}
    ROUTES = []

    def __init__(self, originLong, originLat, destinationLong, destinationLat):
        '''
        Initialize MapRouting instance using origin & destination
        '''
        # if HUB_LOCATION dict is empty
        if len(self.__class__.HUB_LOCATION) == 0:
            self.__class__.read_hub_location()

        # TODO: API request
        for hub in self.__class__.HUB_LOCATION:
            centre = []
            centre.append((originLong+destinationLong+float(self.__class__.HUB_LOCATION[hub]['long']))/3)
            centre.append((originLat+destinationLat+float(self.__class__.HUB_LOCATION[hub]['lat']))/3)
            first = self.__class__.get_half_route(originLong, originLat, float(self.__class__.HUB_LOCATION[hub]['long']), float(self.__class__.HUB_LOCATION[hub]['lat']))
            second = self.__class__.get_half_route(
                float(self.__class__.HUB_LOCATION[hub]['long']), float(self.__class__.HUB_LOCATION[hub]['lat']), destinationLong, destinationLat)
            legs = []
            print(first)
            distance = first['routes'][0]['summary']['distance'] + second['routes'][0]['summary']['distance']
            for i in range(len(first['routes'][0]['segments'][0]['steps'])-1):
                legs.append({
                    "location": first['routes'][0]['segments'][0]['steps'][i]['maneuver']['location']
                })
            for i in range(len(second['routes'][0]['segments'][0]['steps'])-1):
                legs.append(
                    {"location": second['routes'][0]['segments'][0]['steps'][i]['maneuver']['location']})
            self.__class__.ROUTES.append({
                "hub": hub,
                "distance": distance,
                "centre": centre,
                "legs": legs
            })
        # TODO: sorting by distance
        for i in range(len(self.__class__.ROUTES)-1):
            for j in range(len(self.__class__.ROUTES)-i-1):
                if(self.__class__.ROUTES[j]['distance'] > self.__class__.ROUTES[j+1]['distance']):
                    self.__class__.ROUTES[j], self.__class__.ROUTES[j +1] = self.__class__.ROUTES[j+1], self.__class__.ROUTES[j]

        # TODO: store sorted routes in self.directions
        # STORE THE ROUTES IN waypointsForPloting.json (TESTING PURPOSE)
        # file = open(
        #     os.getcwd()+'\\core\\storage\\waypointsForPloting.json', 'w')
        # file.write(json.dumps({"routes": self.__class__.ROUTES}))
        # file.close()

    @classmethod
    def get_half_route(cls, originLong, originLat, destinationLong, destinationLat) -> dict:
        body = {"coordinates": [[originLong, originLat], [
            destinationLong, destinationLat]], "maneuvers": "true", "preference": "shortest"}
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': '5b3ce3597851110001cf62484f37d7fc2f2e497c8bf660dce732e058',
            'Content-Type': 'application/json; charset=utf-8'
        }
        call = requests.post(
            'https://api.openrouteservice.org/v2/directions/driving-car', json=body, headers=headers).json()
        return call

    def get_routes(self) -> dict:
        '''
        Get all routes with defined waypoints in ascending order
        '''
        '''
        Example return data:
        {
            "routes": [
                {
                    "hub": "City-link Express",
                    "distance": XXXX,
                    "legs":[
                        {
                            "start": [x,y],
                            "end": [x,y],
                        }
                        {
                            "start": [x,y],
                            "end": [x,y],
                        }
                    ]
                }, 
                {
                    "hub": "Pos Laju",
                    ...
                },
                ...
            ]
        }
        '''
        return {"routes": self.__class__.ROUTES}

    @classmethod
    def read_hub_location(cls) -> dict:
        '''Read hub locations data into HUB_LOCATION class variable'''
        with open(cls.HUB_LOCATION_JSON_FILE, 'r') as jsonFile:
            cls.HUB_LOCATION = json.load(jsonFile)

        return cls.HUB_LOCATION


if __name__ == "__main__":
    test1 = HubRouting(101.56318183511695, 3.3615395462207878,
                       101.53071480907951, 3.1000170516638885)
