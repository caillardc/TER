import urllib.request as urlr
import json
import pandas
import folium
from folium.plugins import MarkerCluster
from datetime import datetime as dt
import locale

locale.setlocale(locale.LC_TIME, "fr_FR")

moisannee = dt.strftime(dt.now(), "%Y-%m")

url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=evenements-publics-cibul&" \
      "q=&rows=10000&facet=placename&facet=department&facet=region&facet=city&" \
      "facet=date_start&facet=date_end&facet=pricing_info&refine.date_start=" + moisannee

data = json.load(urlr.urlopen(url))

regionlist = [
    'Auvergne-Rhône-Alpes',
    'Bourgogne-Franche-Comté',
    'Bretagne',
    'Centre-Val de Loire',
    'Corse',
    'Grand Est',
    'Hauts-de-France',
    'Île-de-France',
    'Normandie',
    'Nouvelle-Aquitaine',
    'Occitanie',
    'Pays de la Loire',
    "Provence-Alpes-Côte d'Azur",
]
df = pandas.json_normalize(pandas.json_normalize(data, ["records"], max_level=0).loc[:,'fields'])
df.drop(columns = ['image_thumb','city_district','image','free_text', 'timetable', 'lang'], inplace = True)

df = df.loc[df['region'].isin(regionlist),:]
df = df.dropna(subset=["title", "latlon"])



m = folium.Map(location=[45.770799, 3.095003], zoom_start=6)

mc = MarkerCluster()

for row in df.itertuples():
    date_end1 = dt.strftime(dt.strptime(row.date_end, "%Y-%m-%d"), "%d %B %Y")
    date_start1 = dt.strftime(dt.strptime(row.date_start, "%Y-%m-%d"), "%d %B %Y")
    if row.date_end == row.date_start :
        date = date_start1
    else :
        date = date_start1+" au "+date_end1
    style = """
    h3{color : Grey}
    a{color : Black;
    text-decoration:none}
    a:hover{color : Grey}   
            """
    html = """
    <head>
    <style> {}
    </style>
    </head>
    <h3> {} </h3>
    <a href=\"{}\" target=\"_blank\"><h5> {} </h5></a>
    """.format(style, date, row.link, row.title)
    iframe = folium.IFrame(html=html, width=210, height=130)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker(location=row.latlon, popup=popup).add_to(mc)
m.add_child(mc)
m.save('mapBD.html')


