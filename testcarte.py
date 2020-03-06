import folium
# import folium.plugins
#
#
# m = folium.Map(location=[45.5236, -122.6750])
# fg = folium.FeatureGroup()                          # Main group
# g1 = folium.plugins.FeatureGroupSubGroup(fg, 'g1')  # First subgroup of fg
# g2 = folium.plugins.FeatureGroupSubGroup(fg, 'g2')  # Second subgroup of fg
# m.add_child(fg)
# m.add_child(g1)
# m.add_child(g2)
# g1.add_child(folium.Marker([0,0]))
# g2.add_child(folium.Marker([0,1]))
# folium.LayerControl(collapsed=False).add_to(m)
# folium.plugins.MeasureControl().add_to(m)
# m.save('map.html')

import urllib.request as urlr
import json
import pandas
url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-vehicules-position-tr&rows=450&facet=numerobus&facet=nomcourtligne&facet=sens&facet=destination"
basededonnee = json.load(urlr.urlopen(url))

df = pandas.DataFrame([basededonnee['records'][i]['fields'] for i in range(len(basededonnee['records']))])
m = folium.Map(location = [48.146952, -1.705877])
print(df.head(10))
for ligne in range(len(df)):
    folium.Marker(df.loc[ligne,'coordonnees'], name=df.loc[ligne, "idbus"]).add_to(m)
m.save('map.html')