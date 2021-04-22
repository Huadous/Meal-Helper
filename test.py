
import webbrowser as wb
import folium
from folium import CustomIcon
 
 
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
    get_map()