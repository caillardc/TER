import folium
from html_fct import *

m = folium.Map(location=[48.103098,-1.6716781], zoom_start=13)
folium.Marker(location=[48.103098,-1.6716781], icon=folium.Icon(icon="train", prefix="fa"), popup='Gare de Rennes').add_to(m)
folium.Marker(location=[48.105439,-1.6777709], icon=folium.Icon(color="red", icon="subway", prefix="fa"), popup='Métro Charles de Gaulle').add_to(m)

titre = header(h1("Titre du document", {"class" : "titre"}))
texte = article(p("Texte explicatif")+m._repr_html_())
body = body(titre+texte)
page = html(title="Page 1", links_lst=[{"rel" : "stylesheet", "href" : "style1.css"}], body=body)

print(page)
f = open('page1.html','w')
f.write(page)
f.close()


