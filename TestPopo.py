import folium

m = folium.Map(location=[48.103098,-1.6716781], zoom_start=13)
folium.Marker(location=[48.103098,-1.6716781], icon=folium.Icon(icon="train", prefix="fa"), popup='Gare de Rennes').add_to(m)
folium.Marker(location=[48.105439,-1.6777709], icon=folium.Icon(color="red", icon="subway", prefix="fa"), popup='Métro Charles de Gaulle').add_to(m)

m.save('mapTestIcon.html')