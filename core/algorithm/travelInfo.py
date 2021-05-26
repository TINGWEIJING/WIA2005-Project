import requests
import googlemaps
import json
import os
import sys


class GoogleDirectionsRouting:
    # set quota per minute per user to UNLIMITED
    API_KEY = "AIzaSyBKKRxcvNqrV1E89QKSEsvYAVHlJHJDEm8"
    HUB_LOCATION_JSON_FILE = os.getcwd()+'\\core\\storage\\hub_location.json'
    HUB_LOCATION = {}
    ROUTES = []

    def __init__(self, origin, destination):
        # if HUB_LOCATION dict is empty
        if len(self.__class__.HUB_LOCATION) == 0:
            self.__class__.read_hub_location()

        self.origin = origin
        self.destination = destination

        for hub in self.__class__.HUB_LOCATION:
            # lat,long coordinate for waypoint
            waypointCoordinate = f'{self.__class__.HUB_LOCATION[hub]["lat"]},{self.__class__.HUB_LOCATION[hub]["long"]}'

            # get the response from google distance api
            res = self.__class__.get_route(
                origin, destination, waypointCoordinate)

            # centre between the origin, hub and destination (FOR DISPLAYING MAP)
            centre = []
            # number of steps in each path
            stepLength = len(res['routes'][0]['legs'][1]['steps'])
            # append latitude of centre point (sum of 3 lat / 3)
            centre.append((float(res['routes'][0]['legs'][0]['steps'][0]["start_location"]["lat"])+
            self.__class__.HUB_LOCATION[hub]["lat"]+
            float(res['routes'][0]['legs'][1]['steps'][stepLength-1]["start_location"]["lat"]))/3)
            # append longitude of centre point (sum of 3 long / 3)
            centre.append((float(res['routes'][0]['legs'][0]['steps'][0]["start_location"]["lng"])+
            self.__class__.HUB_LOCATION[hub]["long"]+
            float(res['routes'][0]['legs'][1]['steps'][stepLength-1]["start_location"]["lng"]))/3)

            # legs store all the steps for a hub
            legs = []

            # store the distance of (origin->hub) and (hub->destination) in km
            distance = float(res['routes'][0]['legs'][0]['distance']['text'].replace(
                ' km', '')) + float(res['routes'][0]['legs'][1]['distance']['text'].replace(' km', ''))

            originLocation = []
            destinationLocation = []
            # path 0 is (origin->hub), 1 is (hub->destination)
            for path in range(2):
                # loop through all the available steps in each path
                for i in range(len(res['routes'][0]['legs'][path]['steps'])-1):
                    if(path==0 and i==0):
                        originLocation = [res['routes'][0]['legs'][path]['steps'][i]["start_location"]["lat"],
                            res['routes'][0]['legs'][path]['steps'][i]["start_location"]["lng"]]
                    if(i==len(res['routes'][0]['legs'][path]['steps'])-2):
                        destinationLocation = [res['routes'][0]['legs'][path]['steps'][i]["end_location"]["lat"],
                        res['routes'][0]['legs'][path]['steps'][i]["end_location"]["lng"]]

                    start = [res['routes'][0]['legs'][path]['steps'][i]["start_location"]["lat"],
                            res['routes'][0]['legs'][path]['steps'][i]["start_location"]["lng"]]
                    end = [res['routes'][0]['legs'][path]['steps'][i]["end_location"]["lat"],
                        res['routes'][0]['legs'][path]['steps'][i]["end_location"]["lng"]]
                    legs.append({
                        "start": start,
                        "end": end
                    })

            # add the travel information for each hub
            self.__class__.ROUTES.append({
                "hub": hub,
                "origin": originLocation,
                "hubLocation":[self.__class__.HUB_LOCATION[hub]["lat"],self.__class__.HUB_LOCATION[hub]["long"]],
                "destination": destinationLocation,
                "distance": distance,
                "centre": centre,
                "legs": legs
            })

        # bubble sort based on total distance in ASCENDING order
        for i in range(len(self.__class__.ROUTES)-1):
            for j in range(len(self.__class__.ROUTES)-i-1):
                if(self.__class__.ROUTES[j]['distance'] > self.__class__.ROUTES[j+1]['distance']):
                    self.__class__.ROUTES[j], self.__class__.ROUTES[j +
                        1] = self.__class__.ROUTES[j+1], self.__class__.ROUTES[j]

    @classmethod
    def get_route(cls,origin,destination, waypoint)->dict:
        # call the google distance api and return response body in json/dict
        req_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoint}&key={API_KEY}'.format(
            origin=origin, destination=destination, waypoint=waypoint, API_KEY=cls.API_KEY)
        return requests.get(req_url).json()

    def get_routes(self):
        # file = open(os.getcwd()+'\\core\\storage\\waypointsForPloting.json', 'w')
        # file.write(json.dumps({"routes": self.__class__.ROUTES}))
        # file.close()
        return {"routes": self.__class__.ROUTES}

    @classmethod
    def read_hub_location(cls) -> dict:
        '''Read hub locations data into HUB_LOCATION class variable'''
        with open(cls.HUB_LOCATION_JSON_FILE, 'r') as jsonFile:
            cls.HUB_LOCATION = json.load(jsonFile)

        return cls.HUB_LOCATION


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


# OpenRouteService api requires longlat but not latlong
class HubRouting:

    HUB_LOCATION_JSON_FILE = os.getcwd()+'\\core\\storage\\hub_location.json'
    HUB_LOCATION = {}
    ROUTES = []

    def __init__(self, oriLong, oriLat, destLong, destLat, oriAddress: str = None, destAddress: str = None):
        '''
        Initialize MapRouting instance using origin & destination
        '''
        # if HUB_LOCATION dict is empty
        if len(self.__class__.HUB_LOCATION) == 0:
            self.__class__.read_hub_location()

        # if address is used, then convert to coordinates
        if oriAddress and destAddress:
            coord = self.__class__.get_geocode(oriAddress, destAddress)
            oriLat, oriLong, destLat, destLong = coord

        # TODO: API request
        for hub in self.__class__.HUB_LOCATION:
            centre = []
            # center point between 3 three points
            centre.append(
                (oriLong+destLong+float(self.__class__.HUB_LOCATION[hub]['long']))/3)
            centre.append(
                (oriLat+destLat+float(self.__class__.HUB_LOCATION[hub]['lat']))/3)
            # get route
            first = self.__class__.getRoute(oriLong, oriLat, float(self.__class__.HUB_LOCATION[hub]['long']), float(
                self.__class__.HUB_LOCATION[hub]['lat']), destLong, destLat)
            legs = []

            distance = first['routes'][0]['summary']['distance']
            for i in range(len(first['routes'][0]['segments'][0]['steps'])-1):
                legs.append({
                    "location": first['routes'][0]['segments'][0]['steps'][i]['maneuver']['location']
                })
            self.__class__.ROUTES.append({
                "hub": hub,
                "distance": distance,
                "centre": centre,
                "legs": legs
            })
        # TODO: sorting by distance using other algorithms
        for i in range(len(self.__class__.ROUTES)-1):
            for j in range(len(self.__class__.ROUTES)-i-1):
                if(self.__class__.ROUTES[j]['distance'] > self.__class__.ROUTES[j+1]['distance']):
                    self.__class__.ROUTES[j], self.__class__.ROUTES[j +
                                                                    1] = self.__class__.ROUTES[j+1], self.__class__.ROUTES[j]
        # TODO: store sorted routes in self.directions
        # STORE THE ROUTES IN waypointsForPloting.json (TESTING PURPOSE)
        # file = open(
        #     os.getcwd()+'\\core\\storage\\waypointsForPloting.json', 'w')
        # file.write(json.dumps({"routes": self.__class__.ROUTES}))
        # file.close()

    @classmethod
    def getRoute(cls, originLong, originLat, hubLong, hubLat, destinationLong, destinationLat) -> dict:
        body = {"coordinates": [[originLong, originLat], [hubLong, hubLat], [
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
    def get_geocode(oriAddress: str, destAddress: str) -> tuple:
        '''Use google geocode API to obtain coordinate from address'''
        # TODO: add API key
        # TODO: run 'pip install -U googlemaps'
        # TODO: import googlemaps
        gmaps = googlemaps.Client(key='Add Your Key here')
        # TODO: exception handling
        # api call error
        # no result error
        oriResult = gmaps.geocode(oriAddress)
        destResult = gmaps.geocode(destAddress)
        # TODO: test result
        print(oriResult)
        print(destResult)
        # TODO: exception handling
        oriLoc = oriResult["results"][0]["location"]
        destLoc = destResult["results"][0]["location"]
        return (oriLoc["lat"], oriLoc["lng"], destLoc["lat"], destLoc["lng"])

    @classmethod
    def read_hub_location(cls) -> dict:
        '''Read hub locations data into HUB_LOCATION class variable'''
        with open(cls.HUB_LOCATION_JSON_FILE, 'r') as jsonFile:
            cls.HUB_LOCATION = json.load(jsonFile)

        return cls.HUB_LOCATION


if __name__ == "__main__":
    # test1 = HubRouting(101.56318183511695, 3.3615395462207878,
    #                    101.53071480907951, 3.1000170516638885)
    # print(test1.get_routes())
    test1 = GoogleDirectionsRouting(
        "26, Jalan Kejora U5/121A, Taman Puteri Subang", "University of Malaya, Kuala Lumpur")
    print(test1.get_routes())
