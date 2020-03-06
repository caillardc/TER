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
# # folium.plugins.MeasureControl().add_to(m)
# m.save('map.html')

import urllib.request as urlr
import json
import pandas
url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-vehicules-position-tr&rows" \
      "=450&facet=numerobus&facet=nomcourtligne&facet=destination"
basededonnee = json.load(urlr.urlopen(url))

d_lignes = {}
df = pandas.DataFrame([basededonnee['records'][i]['fields'] for i in range(len(basededonnee['records']))])
m = folium.Map(location = [48.146952, -1.705877])


for ligne in range(len(df)):
    malignedeb = df.loc[ligne, 'nomcourtligne']
    if malignedeb not in d_lignes.keys():
        d_lignes[str(malignedeb)] = folium.FeatureGroup(malignedeb)
        d_lignes[str(malignedeb)].add_to(m)
    folium.Marker(df.loc[ligne,'coordonnees'], popup=str(df.loc[ligne, "idbus"])+ str(df.loc[ligne,'destination'])
                  ,icon=folium.Icon(icon='bus', prefix="fa")).add_to(d_lignes[str(malignedeb)])
folium.LayerControl(collapsed=False).add_to(m)
m.save('map.html')