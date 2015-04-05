from xml.dom.minidom import parse
from geojson import Feature, Point


def gpxtojson(file):

    DOMTree = parse(file)
    collection = DOMTree.documentElement

    if 'waypoint' in file:
        root_tag = 'wpt'
        properties = ['ele', 'name', 'desc', 'sym']
    elif 'track' in file:
        root_tag = 'trkpt'
        properties = []

    json_points = []
    waypoints = collection.getElementsByTagName(root_tag)
    for point in waypoints:

        latlng = point.attributes.items()
        new_point = Point([float(x) for _, x in latlng])

        new_properties = {}
        for tag in properties:
            if point.getElementsByTagName(tag):
                data = point.getElementsByTagName(tag)[0].childNodes[0].data
                new_properties[tag] = data

        json_points.append(Feature(geometry=new_point, properties=new_properties))

    return json_points