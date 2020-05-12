import urllib.request as urlr
import json
import pandas
import folium
from folium.plugins import MarkerCluster
from datetime import datetime as dt
import locale

def getDay(year,month):
    if (month in [4,6,9,11]):
        return 30
    elif month == 2:
        if (year % 4 == 0) and (year % 100 != 0) or  (year % 400 == 0):
            return 29
        return 28
    return 31


locale.setlocale(locale.LC_TIME, "fr_FR")

moisannee = dt.strftime(dt.now(), "%Y-%m")
nbjourmois = getDay(int(moisannee[:-3]),int(moisannee[-2:]))

#DATA FRAME

url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=evenements-publics-cibul&" \
      "q=&rows=100&facet=placename&facet=department&facet=region&facet=city&" \
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
df.drop(columns = ['image_thumb','city_district','free_text', 'timetable', 'lang'], inplace = True)
df = df.loc[df['region'].isin(regionlist),:]
df = df.dropna(subset=["title", "latlon"])
df = df.drop_duplicates(['title', 'date_start'])

#CARTE
m = folium.Map(location=[45.770799, 3.095003], zoom_start=6, control_scale=False)

GroupEvenement = MarkerCluster(name="L'ensemble des événements")
group1 =folium.plugins.FeatureGroupSubGroup(GroupEvenement, name="Les évenement du 1 au 6{}"
                                            .format(dt.strftime(dt.now(), "%B")))
group2 =folium.plugins.FeatureGroupSubGroup(GroupEvenement, name="Les évenement du 7 au 12{}"
                                            .format(dt.strftime(dt.now(), "%B")))
group3 =folium.plugins.FeatureGroupSubGroup(GroupEvenement, name="Les évenement du 13 au 18{}"
                                            .format(dt.strftime(dt.now(), "%B")))
group4 =folium.plugins.FeatureGroupSubGroup(GroupEvenement, name="Les évenement du 19 au 24{}"
                                            .format(dt.strftime(dt.now(), "%B")))
group5 =folium.plugins.FeatureGroupSubGroup(GroupEvenement, name="Les évenement du 24 au {}{}"
                                            .format(nbjourmois, dt.strftime(dt.now(), "%B")))

#GRAPHE 1

for row in df.itertuples():

    #CARTE

    date_end1 = dt.strftime(dt.strptime(row.date_end, "%Y-%m-%d"), "%d %B %Y")
    date_start1 = dt.strftime(dt.strptime(row.date_start, "%Y-%m-%d"), "%d %B %Y")
    if row.date_end == row.date_start :
        date = date_start1
    else :
        date = date_start1+" au "+date_end1
    style = """
    body{font-family : calibri;}
    h3{color : Grey}
    a{color : Black;
    text-decoration:none}
    a:hover{color : Grey}
    img{
        width: 28%;
        padding-right: 2%;
    }
    h3{width:70%;}
    h3, img{
        display: inline-block; 
        vertical-align: middle;
    }
    p{font-size: 0.8rem;}
            """
    html = """
    <head>
    <style> {}
    </style>
    </head><body>""".format(style )
    if str(row.image).lower() != 'nan':
        html+= "<a href='{}' target=\"_blank\"><img  src= '{}' alt='Affiche'></a>".format(row.image, row.image)
    html += '<h3> {} </h3>' \
            '<a href=\"{}\" target=\"_blank\"><h5> {} </h5></a>'.format(date,row.link, row.title)
    if str(row.description).lower() != 'nan':
        html += "<p><strong>Description :</strong>  {}".format(row.description)
    if str(row.pricing_info).lower() != 'nan':
        html += "<p><strong>Infos prix :</strong>  {}".format(row.pricing_info)
    if str(row.space_time_info).lower() != 'nan':
        html += "<p><strong>Infos lieu et moment :</strong>  {}".format(row.space_time_info)
    html += '</body>'
    iframe = folium.IFrame(html=html, height=130)
    popup = folium.Popup(iframe, max_width=500, min_width=250)

    if int(dt.strftime(dt.strptime(row.date_start, "%Y-%m-%d"), "%d")) in range(1,7):
        folium.Marker(location=row.latlon, popup=popup,icon=folium.Icon(icon='info', prefix='fa')).add_to(group1)
    elif int(dt.strftime(dt.strptime(row.date_start, "%Y-%m-%d"), "%d")) in range(7,13):
        folium.Marker(location=row.latlon, popup=popup,icon=folium.Icon(icon='info', prefix='fa')).add_to(group2)
    elif int(dt.strftime(dt.strptime(row.date_start, "%Y-%m-%d"), "%d")) in range(13,19):
        folium.Marker(location=row.latlon, popup=popup,icon=folium.Icon(icon='info', prefix='fa')).add_to(group3)
    elif int(dt.strftime(dt.strptime(row.date_start, "%Y-%m-%d"), "%d")) in range(19,24):
        folium.Marker(location=row.latlon, popup=popup,icon=folium.Icon(icon='info', prefix='fa')).add_to(group4)
    else:
        folium.Marker(location=row.latlon, popup=popup,icon=folium.Icon(icon='info', prefix='fa')).add_to(group5)
    #GRAPHE 1


m.add_child(GroupEvenement), m.add_child(group1), m.add_child(group2)
m.add_child(group3),  m.add_child(group4), m.add_child(group5)
folium.LayerControl(collapsed=True).add_to(m)
m.save('mapBD.html')


