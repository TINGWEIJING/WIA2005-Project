# Import gmplot library.
from gmplot import *
# Place map
# First two arugments are the geogrphical coordinates .i.e. Latitude and Longitude
#and the zoom resolution.
# klang - 3.0346383, 101.3741497
gmap = gmplot.GoogleMapPlotter(3.0346383, 101.3741497, 18)
# Coordinates - path one
# { "lat": 3.3616847, "lng": 101.5634998 }
# { "lat": 3.0346383, "lng": 101.3741497 }
# { "lat": 3.10012, "lng": 101.5309481 }
path_one_lats, path_one_longs = zip(
    *[
        (3.3616847, 101.5634998), (3.0346383, 101.3741497), (3.10012, 101.5309481),
    ]
)
gmap.plot(path_one_lats, path_one_longs, "cornflowerblue", edge_width=3.0)

# Location where you want to save your file.
gmap.draw("../templates/map3.html")