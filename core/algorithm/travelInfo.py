import requests
import googlemaps
import json
import os
import sys
from collections import OrderedDict
import math as math


class GoogleDirectionsRouting:
    # set quota per minute per user to UNLIMITED
    # API_KEY = "AIzaSyBKKRxcvNqrV1E89QKSEsvYAVHlJHJDEm8"
    API_KEY = "AIzaSyA6cAGqGi60aw4-sIFeKIj-JvtFfNV5X1c"
    HUB_LOCATION_JSON_FILE = os.getcwd()+'\\core\\storage\\hub_location.json'
    HUB_LOCATION = {}

    def __init__(self, origin, destination):
        # if HUB_LOCATION dict is empty
        if len(self.__class__.HUB_LOCATION) == 0:
            self.__class__.read_hub_location()

        self.origin = origin
        self.destination = destination
        self.routes = []
        # return
        for hub in self.__class__.HUB_LOCATION:
            # lat,long coordinate for waypoint
            print(hub)
            waypointCoordinate = f'{self.__class__.HUB_LOCATION[hub]["lat"]},{self.__class__.HUB_LOCATION[hub]["long"]}'

            # get the response from google distance api
            res = self.__class__.get_route(origin, destination, waypointCoordinate)
            # print(res)

            # if not result
            if(res['status'] == "ZERO_RESULTS" or res['status'] == "OVER_QUERY_LIMIT"):
                print('no result, maybe we run out of credit')
                print(res['status'])
                # self.routes = []
                # break
                continue
            else:
                print('we got the result for 1 company')
                print(res['status'])
            # legs store all the steps for a hub
            legs = []

            # DEBUG
            # print(res['routes'])
            # store the distance of (origin->hub) and (hub->destination) in km
            distance = float(res['routes'][0]['legs'][0]['distance']['text'].replace(
                ' km', '')) + float(res['routes'][0]['legs'][1]['distance']['text'].replace(' km', ''))

            originLocation = []
            destinationLocation = []
            # path 0 is (origin->hub), 1 is (hub->destination)
            for path in range(2):
                # loop through all the available steps in each path
                for i in range(len(res['routes'][0]['legs'][path]['steps'])):
                    if(path == 0 and i == 0):
                        originLocation = [res['routes'][0]['legs'][path]['steps'][i]["start_location"]["lat"],
                                          res['routes'][0]['legs'][path]['steps'][i]["start_location"]["lng"]]
                    if(i == len(res['routes'][0]['legs'][path]['steps'])-1):
                        destinationLocation = [res['routes'][0]['legs'][path]['steps'][i]["end_location"]["lat"],
                                               res['routes'][0]['legs'][path]['steps'][i]["end_location"]["lng"]]
                    start = [res['routes'][0]['legs'][path]['steps'][i]["start_location"]["lat"],
                             res['routes'][0]['legs'][path]['steps'][i]["start_location"]["lng"]]
                    end = [res['routes'][0]['legs'][path]['steps'][i]["end_location"]["lat"],
                           res['routes'][0]['legs'][path]['steps'][i]["end_location"]["lng"]]
                    legs.append({
                        "start":start,
                        "end":end,
                        "polyline": res['routes'][0]['legs'][path]['steps'][i]["polyline"]
                    })

            # add the travel information for each hub
            self.routes.append({
                "hub": hub,
                "origin": originLocation,
                "hubLocation": [self.__class__.HUB_LOCATION[hub]["lat"], self.__class__.HUB_LOCATION[hub]["long"]],
                "destination": destinationLocation,
                "distance": distance,
                "path1_distance": float(res['routes'][0]['legs'][0]['distance']['text'].replace(' km', '')),
                "path2_distance": float(res['routes'][0]['legs'][1]['distance']['text'].replace(' km', '')),
                "legs": legs
            })
        
        self.introsort()

    @classmethod
    def get_route(cls, origin, destination, waypoint) -> dict:
        # call the google distance api and return response body in json/dict
        req_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoint}&key={API_KEY}'.format(
            origin=origin, destination=destination, waypoint=waypoint, API_KEY=cls.API_KEY)
        req = requests.get(req_url).json()
        return req

    def get_routes(self):
        res = {"routes": self.routes}
        return res

    def get_sorted_routes(self):
        # return sorted Ordered Dict
        
        # DEBUG IN
        # with open('data.json', 'r') as outfile:
        #     self.sorted_routes = json.load(outfile)
        # DEBUG OUT
        with open('data.json', 'w') as outfile:
            json.dump(self.sorted_routes, outfile, indent=4)
        return self.sorted_routes

    @classmethod
    def read_hub_location(cls) -> dict:
        '''Read hub locations data into HUB_LOCATION class variable'''
        with open(cls.HUB_LOCATION_JSON_FILE, 'r') as jsonFile:
            cls.HUB_LOCATION = json.load(jsonFile)

        return cls.HUB_LOCATION

    # Start for introsort
    def introsort(self) -> OrderedDict:
        # build a tester list so that can sort easier
        self.temp = self.routes
        self.tester = list()
        list1 = []
        for i in range(0, len(self.temp)):
            list1.append(self.temp[i]['hub'])
        list2 = []
        for i in range(0, len(self.temp)):
            list2.append(self.temp[i]['distance'])
        for i in range(0, len(list1)):
            self.tester.append([list1[i], list2[i]])

        # calculate the maxdepth using the formula log(length(A)) × 2
        maxdepth = (len(self.tester).bit_length() - 1)*2
        # call recursion method
        self.introsort_recur(0, len(self.tester), maxdepth)
        self.build_Ordered_Dict()

    def introsort_recur(self, start, end, maxdepth):
        if end - start <= 1:
            # no need sort since only 0/1 element
            return
        elif maxdepth == 0:
            self.heapsort(start, end)
        else:
            # find partition
            p = self.partition(start, end)
            # quick sort the left part
            self.introsort_recur(start, p+1, maxdepth-1)
            # quick sort the right part
            self.introsort_recur(p+1, end, maxdepth-1)

    def partition(self, start, end):
        pivot = self.tester[start][1]
        i = start - 1
        j = end

        while True:
            # bring the pivot to its appropiate position such that
            i = i + 1
            # left of the pivot is smaller
            while self.tester[i][1] < pivot:
                i = i + 1
            j = j - 1
            # right of the pivot is larger
            while self.tester[j][1] > pivot:
                j = j - 1

            if i >= j:
                return j
            else:
                self.tester[i], self.tester[j] = self.tester[j], self.tester[i]

    def heapsort(self, start, end):
        self.build_max_heap(start, end)
        for i in range(end-1, start, -1):
            # swap the root node with last node
            self.tester[i], self.tester[start] = self.tester[start], self.tester[i]
            self.max_heapify(index=0, start=start, end=i)

    def build_max_heap(self, start, end):
        length = end - start
        index = (length-1)-1//2
        while index >= 0:
            self.max_heapify(index, start, end)
            index = index - 1

    def max_heapify(self, index, start, end):
        size = end - start
        left = 2*index + 1
        right = 2*index + 2
        if (left < size and self.tester[start+left][1] > self.tester[start+index][1]):
            largest = left
        else:
            largest = index
        if (right < size and self.tester[start+right][1] > self.tester[start+largest][1]):
            largest = right
        if largest != index:
            self.tester[start + largest], self.tester[start + index] = self.tester[start + index], self.tester[start + largest]
            self.max_heapify(largest, start, end)

    def build_Ordered_Dict(self) -> OrderedDict:
        sorted_hub_index = { hub_name: i for i, (hub_name, distance) in enumerate(self.tester)}
        routes = self.get_routes()
        sorted_route_list = [0] * len(self.tester)
        # file = open(os.getcwd()+'\\core\\storage\\temp.json', 'w')
        # file.write(json.dumps(self.get_routes()))
        # file.close()
        # print(sorted_hub_index)
        for hub_obj in routes.get('routes'):
            hub_name = hub_obj.get('hub')
            sorted_route_list[sorted_hub_index.get(hub_name)] = hub_obj
        
        self.sorted_routes = {'routes':sorted_route_list}

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
    print("this shouldn't be printed")
    # print(test1.get_sorted_routes())
