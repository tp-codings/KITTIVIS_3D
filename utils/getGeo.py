import overpy
import sys
from geopy.geocoders import Nominatim

def get_maxspeed(lat, lon, radius):
    api = overpy.Overpass()

# fetch all ways and nodes
    result = api.query("""
            way(around:""" + radius + """,""" + lat  + """,""" + lon  + """) ["maxspeed"];
                (._;>;);
                    out body;
                        """)
    results_list = []
    for way in result.ways:
        road = {}
        road["name"] = way.tags.get("name", "n/a")
        road["speed_limit"] = way.tags.get("maxspeed", "n/a")
        nodes = []
        for node in way.nodes:
            nodes.append((node.lat, node.lon))
        road["nodes"] = nodes
        results_list.append(road)
    return extract_first_speed_limit(results_list)

def extract_first_speed_limit(data):
    # Überprüfe, ob die Daten vorhanden sind und mindestens ein Element enthalten
    if not data or len(data) == 0:
        return None
    # Extrahiere das Geschwindigkeitslimit des ersten Elements
    first_speed_limit = data[0].get("speed_limit")
    return first_speed_limit

def get_location(lat, lon):
    geolocator = Nominatim(user_agent="GetLoc", timeout=None)
    location = geolocator.reverse((lat, lon), language='de')
    address = location.address if location else "Unbekannter Ort"
    print(address)
    return address


if __name__ == "__main__":
    result = get_maxspeed(sys.argv[1], sys.argv[2], sys.argv[3])
    print(result)