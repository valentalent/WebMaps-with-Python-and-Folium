import folium
import pandas as pd

def color_producer(elevation):
    if(elevation<1000):
        return 'green'
    elif(elevation<2000):
        return 'orange'
    else:
        return 'red'

df1=pd.read_csv("volcanos.csv")
#taking columns we need and saving it into lists
lon = list(df1["LON"])
lat = list(df1["LAT"])
elev = list(df1["ELEV"])

#object map
map=folium.Map(location=[38,-99 ], zoom_start=6, tiles="Stamen Terrain")

#featuregroup
fgv = folium.FeatureGroup(name="Volcanoes")

#child
#zip koristimo za iteraciju kroz dvije ili više lista
#javi grešku zbog el jer je float, a treba biti string, str(el) bi riješilo problem, ali ima navodnike pa
#treba dodati html parser od foliuma

for lt, ln, el in zip(lat,lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=10, popup=folium.Popup(str(int(el)),
    parse_html=True), fill_color=color_producer(el), color='grey', fill_opacity=0.65))

fgp = folium.FeatureGroup(name="Population")

#dodaje poligone za zemlje na temelju "MultiPolygona" iz json file-a
#također boja zemlje određenog stanovništva na temelje properties-pop2005

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'red' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
#dodajemo layercontrol, ali moramo dodati i feature group, zato je ispod njega
map.add_child(folium.LayerControl())

map.save("Map1.html")

