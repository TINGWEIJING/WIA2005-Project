import requests

API_KEY = ""

def direction(origin,destination):
    # Get all the alternatives route
    req_url = 'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&alternatives=true&key={}'.format(origin,destination,API_KEY)
    x = requests.get(req_url)