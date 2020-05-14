import urllib.request as urlr
import json
import pandas
import folium
from folium.plugins import MarkerCluster
from datetime import datetime as dt
import locale
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.palettes import Category20
from bokeh.embed import components
import os


def getDay(year, month):
    if month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        if (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0):
            return 29
        return 28
    return 31


locale.setlocale(locale.LC_TIME, "fr_FR")

moisannee = dt.strftime(dt.now(), "%Y-%m")
nbjourmois = getDay(int(moisannee[:-3]),int(moisannee[-2:]))

#DATA FRAME

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
df.drop(columns = ['image_thumb','city_district','free_text', 'timetable', 'lang'], inplace = True)
df = df.loc[df['region'].isin(regionlist),:]
df = df.dropna(subset=["title", "latlon"])
df = df.drop_duplicates(['title', 'date_start'])

#CARTE
m = folium.Map(location=[45.770799, 3.095003], zoom_start=5, control_scale=False)

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
dicocol = {}
for region in regionlist:
    dicocol[region] = 0

#GRAPHE 2
dicojour = {}
for jour in range(1,nbjourmois+1):
    dicojour[jour] = 0

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
    for region in dicocol.keys():
        if str(row.region) == region:
             dicocol[region] += 1

    #GRAPHE 2
    for jour in dicojour.keys():
        if int(dt.strftime(dt.strptime(row.date_start, "%Y-%m-%d"), "%d")) == int(jour):
            dicojour[jour] += 1


#CARTE
m.add_child(GroupEvenement), m.add_child(group1), m.add_child(group2)
m.add_child(group3),  m.add_child(group4), m.add_child(group5)
folium.LayerControl(collapsed=True).add_to(m)

htmlcarte = m._repr_html_()

#GRAPHE 1

source = ColumnDataSource(data=dict(region= list(dicocol.keys()), counts=list(dicocol.values()), color=Category20[13]))
p = figure(x_range=regionlist, sizing_mode="stretch_width", height=500, title=None,
           toolbar_location=None, tooltips=[("Nombre d'événement", '@counts')], margin=(10,30))
p.vbar(x='region', top='counts', width=0.8, color='color', source=source)
p.xaxis.major_label_orientation = 1
scriptgraph1, divgraph1 = components(p)

#GRAPHE 2

source = ColumnDataSource(data=dict(x= list(dicojour.keys()), y=list(dicojour.values())))
p2 = figure(sizing_mode="stretch_width", height=500, title=None, toolbar_location=None,
            tooltips=[("Nombre d'événement", '@y')],margin=(20,10))
p2.line(x='x', y='y', source=source, line_width=4)
scriptgraph2, divgraph2 = components(p2)

#QUELQUE CHIFFRE

nbevenement = len(df)
regionmax = ''
maxi = 0
for region,val in dicocol.items():
    if val > maxi:
        regionmax = region
        maxi = val

#PARTIE SITE

CodeHTML = """
<!DOCTYPE html>
<html>
 <head>
   <meta charset="UTF-8">
   <link rel="shortcut icon" href="https://image.flaticon.com/icons/svg/2904/2904713.svg">
   <link rel="stylesheet" type="text/css" href="style.css" />
   <script type="text/javascript" src="https://cdn.bokeh.org/bokeh/release/bokeh-2.0.2.min.js"\
    integrity="sha384-ufR9RFnRs6lniiaFvtJziE0YeidtAgBRH6ux2oUItHw5WTvE1zuk9uzhUU/FJXDp" crossorigin="anonymous"></script>
   <title> Représentation graphique </title>
   {scriptg1}
   {scriptg2}
 </head>
 <body>
  <header>
   <div id = "titre"> 
   <img src="https://image.flaticon.com/icons/svg/2904/2904713.svg" alt="Logo"><h1>
   Représentation graphique de l'api évenement
   </h1></div><div id= "menu"><div class= "container"><nav>
    <ul><li><a href="#zonechiffre">
    Les chiffres
    </a></li><li><a href="#zonecarte">
    La carte
    </a></li><li><a href="#first">
    Le premier graphe
    </a></li><li><a href="#second">
    Le second graphe
    </a></li>
    </ul>
   </nav></div></div>
  </header>
  <article>
  <div id= "zonechiffre"><div class= "container">
  <div class='bloc bloc1'>
  <img src="https://image.flaticon.com/icons/svg/2693/2693507.svg" alt="Event"><div class='txtpre'><p id='firsttxt'>
  {nbevent}<span id='vertical'>ÉVENEMENTS</span>
  </p><p id='last'>
  dans toute la France en {mois} {annee}
  </p></div></div><div class='bloc bloc2'>
  <img src="https://image.flaticon.com/icons/svg/1871/1871058.svg" alt="Carte"><div class='txtpre'><p id='region'>
  {region}
  </p><p id='textedessous'>
  est la région de france qui a organisé le plus d'évenements en {mois} {annee}
  </p></div></div><div class='bloc bloc3'>
  <img src="https://image.flaticon.com/icons/svg/2856/2856740.svg" alt="Saison"><div class='txtpre'><p id="textedessus">
  Le jour où il y le plus d'évenement organisé est: <span id='saison'>16&nbsp{moismaj} </span>
  </p></div></div></div></div>
  
  <div id= "zonecarte"><div class= "container">
  <div class="bloc bloc1"><div class= "texte"><h3>
  Voici une carte des événements du mois de {mois} en France:
  </h3><p>
  Cette carte représente les événements ayant lieu en France qui commence au mois de {mois} {annee}.
  Vous pouvez trier les événements selon leur dates de début. Pour avoir plus d'information sur un événement il
  suffit de cliquer sur l'icone de celui-ci.
  </p></div></div><div class="bloc carte"><div id='lacarte'>
  {carte}
  </div></div></div></div>
  
  <div class= "zonegraph" id= "first"><div class= "container">
  <div class="bloc graph">
  <div class = "legraph">{divg1}
  </div></div><div class="bloc bloc1"><div class= "texte"><h3>
  Les évenements par régions :
  </h3><p>
  Vous pouvez voir ci-contre le nombre d'évenement par jour durant le mois de {mois} {annee}
  en fonction de leur date de début.
  </p></div></div></div></div>
  
  <div class= "zonegraph" id= "second"><div class= "container">
  <div class="bloc bloc1"><div class= "texte"><h3>
  Les événements par dates :
  </h3><p>
  Le graphe suivant représente le nombre d'évenement par region durant le mois de {mois} {annee}
  </p></div></div><div class="bloc graph"><div class = "legraph">{divg2}
  </div></div></div></div></article><footer><div class= "texte"><p>
  © Site web du TER réalisé par Rémi Leduc, Mélanie Guillouet, Clément Caillard, Pauline Hamon-Giraud
  </p></div></footer>
 </body>
</html>
""".format(scriptg1=scriptgraph1, scriptg2=scriptgraph2, carte=htmlcarte, divg1=divgraph2, divg2=divgraph1,
           nbevent=nbevenement, mois=dt.strftime(dt.now(), "%B"), annee=dt.strftime(dt.now(), "%Y"),
           moismaj=dt.strftime(dt.now(), "%B").upper(), region=regionmax.upper())

try:
    os.mkdir('site')
except OSError:
    pass

fp = open(os.path.join('site', 'index.html'), 'w', encoding='UTF-8')
fp.write(CodeHTML)
fp.close()

#CODE CSS

CodeCSS = """
body{
	margin:0;
}

header {
	box-shadow: 0 0.2rem 0.5rem rgba(0, 0, 0, 0.3);
	display: grid;
	grid-template-areas: 'I R S';
	align-items: center; 
	position: fixed;
	z-index: 1;
	width: 100%;
	background: white;
	height:auto;
}
article {
	padding-top: 4.8rem;
}
header > #titre {
	grid-area: I;
	padding-left: 5%;
	width: 100%
}

header > #titre h1 {
	text-align: center;
	font-family: calibri;
	width:85%;
}

header > #titre h1, header > #titre img{
	display: inline-block;
	vertical-align: middle;
}
header > #titre img{
	max-width: 50px;
	width: 10%;
}

#menu {
	grid-area: S;

}
#menu .container{
	margin-right:3rem;
}
nav ul {
    list-style-type: none;
}

nav a {
	display: block;
	text-decoration: none;
	color: rgb(67, 67, 67);
	font-family: Tahoma;
}

nav li{
	width: 20%;
	text-align:center;
	display: table-cell;
	vertical-align: middle;
	height: 3rem;
	padding: 0 1rem;
}

#zonechiffre {
	background: rgb(246, 193, 71);
	border-bottom: 1px solid #ddd;
	padding: 2rem 5%;
}

#zonechiffre > .container > .bloc {
	position: relative;
	display: inline-block;
	vertical-align: middle;
	width: 32%;
	border-right: 1px solid white;
	height: 100%;
}

#zonechiffre > .container > .bloc.bloc3 {
	border: none;
}

#zonechiffre > .container > .bloc > .txtpre, #zonechiffre > .container > .bloc img{
	display: inline-block;
	vertical-align: middle;	
}

#zonechiffre > .container > .bloc > .txtpre{
	width: 50%;
}
#zonechiffre > .container > .bloc.bloc1 > .txtpre {
	width:60%;
}
#zonechiffre > .container > .bloc img{
	max-width: 8rem;
	width: 20%;
	margin-right: 5%;
	margin-left: 15%;
}
p#firsttxt, #vertical, {
	display: inline-block;
	vertical-align: middle;
}
#zonechiffre > .container > .bloc p {
	font-family:calibri;
	margin: 0;
}
#zonechiffre > .container > .bloc p#firsttxt{
	color: black;
	font-size: 7em;
	width:100%;
}
@media(max-width: 1500px) {
	#zonechiffre > .container > .bloc p#firsttxt{
		font-size: 5rem;
	}
	#vertical{
		font-size: 0.8rem;
	}
 }
 
@media(max-width: 1200px) {
	#zonechiffre > .container > .bloc {
		position: relative;
		display: block;
		width: 100%;
		border-right: none;
		border-bottom: 1px solid white;
		padding: 2rem 0;
	}

	#zonechiffre > .container > .bloc.bloc3 {
		border: none;
	}
	#zonechiffre > .container > .bloc p#firsttxt{
		font-size: 6rem;
	}
	#vertical{
		font-size: 1rem;
	}
	
	#zonechiffre > .container > .bloc > .txtpre{
		width: 60%;
	}	
}
#zonechiffre > .container > .bloc span#vertical{
	color: white;
	writing-mode: sideways-lr;
	font-size: 1rem;
}

#zonechiffre > .container > .bloc p#last{
	color: #424952;
	font-size: 1rem;
}

#zonechiffre > .container > .bloc p#region{
	color: white;
	font-size: 2rem;
	margin-top: 1rem;
}

#zonechiffre > .container > .bloc p#textedessous{
	color: #424952;
	font-size: 1.3rem;
}

 #zonechiffre > .container > .bloc #saison{
	color: black;
	font-size: 4rem;
 }


#zonechiffre > .container > .bloc p#textedessus{
	color: white;
	font-size: 1.5rem;
	margin-top: 1rem;
}

#zonecarte > .container {
	padding-top: 2rem;
	padding-bottom: 2rem; 
	border-bottom: 1px solid #ddd;
}

#zonecarte > .container > .bloc {
	position: relative;
	display: inline-block;
	vertical-align: middle;
}
#zonecarte > .container > .bloc.bloc1 {
	width : 30%;
	min-height: 500px;
}
#zonecarte > .container > .bloc.bloc.carte {
	width : 70%;
}

#zonecarte > .container > .bloc > #lacarte {
	position:relative;
	width:90%;
	height: 100%;
	left: 2rem;
	border:none;
	box-shadow: 0.1rem 0.3rem 0.3rem rgba(0, 0, 0, 0.15);
}

.container > .bloc > .texte h3 {
    font-size: 1.8rem;
    font-weight: 600;
    line-height: 1.4; 
	font-family: calibri;
	color: #424952;
}  
	  
.container > .bloc > .texte p {
	font-size: 1.1rem;
	line-height: 1.6;
	font-family: Tahoma;
	color: #424952;
}
.container > .bloc > .texte {
    position: absolute;
    top: 50%;
	left: 50%;
    margin-right: -50%;
	transform: translate(-50%, -50%);
	width: 70%;
	
}

@media(max-width: 1000px) {
    #zonecarte > .container > .bloc.bloc1 {
        width : 50%;
    }
    #zonecarte > .container > .bloc.bloc.carte {
        width : 50%;
    }
    .container > .bloc > .texte h3 {
        font-size: 1.4rem;
    }  
          
    .container > .bloc > .texte p {
        font-size: 0.8rem;
    }
}

.zonegraph#first {
	position: relative;
	background: #e6f1f3;
}

.zonegraph > .container {
  padding-top: 2rem;
  padding-bottom: 2rem; 
  border-bottom: 1px solid #ddd;
}

#second > .container {
	border-bottom: none;
}
.zonegraph > .container > .bloc {
	position: relative;
	display: inline-block;
	vertical-align: top;
	height: 500px;

}
.zonegraph > .container > .bloc.graph {
	width: 60%;
}
.zonegraph > .container > .bloc.bloc1 {
    width: 40%;
}

.zonegraph > .container > .bloc.graph .legraph{
	position: absolute;
	width:90%;
    top: 50%;
	left: 50%;
    margin-right: -50%;
	transform: translate(-50%, -50%);
	box-shadow: 0.1rem 0.3rem 0.3rem rgba(0, 0, 0, 0.15);
	background-color: white;
	
}

footer .texte{
	position: relative;
	text-align: center;
	height: 4rem;
	background: rgb(66, 73, 82);
	padding-top: 0.8rem;
	overflow: hidden;

}

footer p {
	height: 100%;
	font-family: Roboto, Helvetica, Arial, sans-serif;
	color: rgb(255, 255, 255);
}
"""

fp = open(os.path.join('site', 'style.css'), 'w', encoding='utf-8')
fp.write(CodeCSS)
fp.close()
