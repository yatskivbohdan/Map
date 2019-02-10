import folium
from mymodule import read
import os
from geopy.geocoders import Bing
from geopy.extra.rate_limiter import RateLimiter


os.chdir(os.path.realpath(__file__)[:-7])


read.read_f("locations.list", "data.csv")
year = input("Enter a year:")
data = open("data.csv", 'r', errors = 'ignore')
dict = {}
for line in data:
    if line[:4] == year:
        try:
            com_ind = line[5:].index(",")
            name = line[5:5+com_ind]
            if line[6+com_ind:].count(",") <= 1:
                place = line[6+com_ind:]
            else:
                place = ",".join(line[6+com_ind:].split(",")[-2:])[1:]
            if place not in dict:
                dict[place]=(name)
            elif name not in dict[place]:
                dict[place]+= "," + name
        except:
            pass
map = folium.Map(zoom_start=1)
fg_m = folium.FeatureGroup(name='Movies locations ' + year)
geolocator = Bing("AhIHYq_lkTbr8aO0OobYnJkFJVVUwnxjH18nJBHul38z5qEwn985vF4HqFoi4QMW")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
for key in dict:
    try:
        loc = geolocator.geocode(key)

        fg_m.add_child(folium.Marker(location=[loc.latitude, loc.longitude],
                                    popup=dict[key],
                                    icon=folium.Icon()))
    except:
        pass
fg_p = folium.FeatureGroup(name = "Population")
fg_p.add_child(folium.GeoJson(data = open('world.json', 'r',
                encoding = 'utf-8-sig').read(), style_function = lambda x:{
    'fillColor': 'green' if x ['properties']['POP2005'] < 10000000
    else 'yellow' if 10000000 <= x['properties']['POP2005'] < 40000000
    else 'orange' if 40000000 <= x['properties']['POP2005'] < 100000000
    else 'red'}))

map.add_child(fg_p)
map.add_child(fg_m)
map.add_child(folium.LayerControl())
map.save('Map.html')
