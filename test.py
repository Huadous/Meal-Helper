
import webbrowser as wb
import folium
from folium import CustomIcon

import numpy as np
import pandas as pd
 
 
def draw_custom_icon(map, loc):
     
    marker = folium.Marker(
        location=[25.0431, 121.539723], 
        icon=folium.Icon(color="red",icon="glyphicon glyphicon-cutlery"))
        # folium.Marker(
        # location=[25.0431, 121.539723], 
        # icon=folium.Icon(color="red",icon="fa-truck", prefix='fa')).add_to(m)
 
    map.add_child(marker)
 
 
def get_map():
    loc = [30., 104.]
    map = folium.Map(loc,  # 地图中心
                     tiles='OpenStreetMap',  # stamentoner,Stamen Watercolor,OpenStreetMap'
                     zoom_start=6)
 
    draw_custom_icon(map, loc)
 
    map.save('m.html')
    wb.open('m.html')
 




if __name__ == '__main__':
    # get_map()


    center_point = [40.72796324125046, -73.97619992872274]

    data = (
        np.random.normal(size=(100, 2)) *
        np.array([[.5, .5]]) +
        np.array([center_point])
    )

    df = pd.DataFrame(data, columns=['Lat', 'Long'])


    m = folium.Map(df[['Lat', 'Long']].mean().values.tolist())

    for lat, lon in zip(df['Lat'], df['Long']):
        folium.Marker([lat, lon]).add_to(m)


    sw = df[['Lat', 'Long']].min().values.tolist()
    ne = df[['Lat', 'Long']].max().values.tolist()

    m.fit_bounds([sw, ne]) 
    m.save('test.html') 