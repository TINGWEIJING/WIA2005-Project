# Import gmplot library.
from gmplot import *
# Place map
# First two arugments are the geogrphical coordinates .i.e. Latitude and Longitude
#and the zoom resolution.
gmap = gmplot.GoogleMapPlotter(17.438139, 78.39583, 18)
# Location where you want to save your file.
gmap.draw("../templates/map3.html")