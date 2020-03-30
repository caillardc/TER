import folium
import html_fct

m = folium.Map(location=[48.103098,-1.6716781], zoom_start=13)
folium.Marker(location=[48.103098,-1.6716781], icon=folium.Icon(icon="train", prefix="fa"), popup='Gare de Rennes').add_to(m)
folium.Marker(location=[48.105439,-1.6777709], icon=folium.Icon(color="red", icon="subway", prefix="fa"), popup='Métro Charles de Gaulle').add_to(m)

titre = html_fct.header(html_fct.h1("Titre du document"))
texte = html_fct.article(html_fct.p("Texte explicatif")+m._repr_html_())
body = html_fct.body(titre+texte)
page = html_fct.html(title="Page 1", links_lst=[{"rel" : "stylesheet", "href" : "style1.css"}], body=body)

print(page)
f = open('page1.html','w')
f.write(page)
f.close()


