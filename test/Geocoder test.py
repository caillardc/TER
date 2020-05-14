# Installer geocoder avec la commander: "pip install geocoder"
import geocoder

g = geocoder.osm('New York city')
print(g.latlng)