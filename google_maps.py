import requests
import re

API_key = "AIzaSyDYSOjkiATtDpW9qEIOPsbjwvdPqSuIEdA"
COOR_DIFF = 0.00009 * 5  # 10m * n

# TODO: replace with the real data imported vis CSV or other format (depending on the requirement)
data = [
    ["POINT (174.4513638653 -36.8860243241)", "BETHELLS RD (WCC)"],
    ["POINT (174.4497720357 -36.8913620998)", "BETHELLS RD (WCC)"],
    ["POINT (174.556297882 -37.0165364501)", "WHATIPU RD"],
    ["POINT (174.4712833983 -36.9534253801)", "SEAVIEW RD (PIHA)"],
    ["POINT (174.5438302975 -36.9442337643)", "PIHA RD"],
    ["POINT (174.4801522996 -36.9775084447)", "KAREKARE RD"],
    ["POINT (174.4699737384 -36.9573123506)", "BEACH VALLEY RD"],
    ["POINT (174.7312755423 -37.1828783774)", "GLENBROOK BEACH RD"],
    ["POINT (175.056786306 -36.9781819942)", "CLEVEDON-KAWAKAWA RD"],
    ["POINT (175.000106141 -36.9285970881)", "WAIKOPUA RD"],
    ["POINT (174.9726129099 -36.9410602158)", "WHITFORD-MARAETAI RD"],
    ["POINT (174.9097212116 -36.871404902)", "EASTERN BEACH RD"],
    ["POINT (174.9110686595 -36.8818525921)", "BUCKLANDS BEACH RD"],
]


def process_road_names(road_names):
    proc_road_names = []
    for name in road_names:
        index_rd = name.find(" RD")
        index_st = name.find(" ST")
        index = max(index_rd, index_st)
        if index != -1:
            proc_road_names.append(name[: index + 3])
        else:
            proc_road_names.append(name)
    return proc_road_names


def process_WKT(WKT):
    coordinate = WKT.strip("POINT ()").split()
    latitude = float(coordinate[1])
    longitude = float(coordinate[0])
    return latitude, longitude


def make_coordinates(latitude, longitude):
    north = [latitude + COOR_DIFF, longitude]
    south = [latitude - COOR_DIFF, longitude]
    east = [latitude, longitude + COOR_DIFF]
    west = [latitude, longitude - COOR_DIFF]
    return f"{latitude}%2C{longitude}%7C{north[0]}%2C{north[1]}%7C{south[0]}%2C{south[1]}%7C{east[0]}%2C{east[1]}%7C{west[0]}%2C{west[1]}"


def get_address(place_id):
    endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"fields": "formatted_address", "place_id": place_id, "key": API_key}
    url = endpoint + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        formatted_address = data.get("result").get("formatted_address")
        return formatted_address
    else:
        print("Error:", response.status_code)
        return []


def get_snap_to_roads(path):
    endpoint = "https://roads.googleapis.com/v1/snapToRoads"
    params = {"interpolate": "true", "key": API_key, "path": path}
    url = endpoint + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        snapped_points = data.get("snappedPoints")
        return snapped_points
    else:
        print("Error:", response.status_code)
        return []


def extract_road_name(address):
    pattern = r"\b(?:\d+\s+)?(.*?)(?:\s+Road|Street)\b"
    match = re.search(pattern, address)

    if match:
        return match.group(1)
    else:
        print("Error: Failed to extract road names")
        return ""


# TODO: variable names are poorly named, fix later
def is_correct_addr(road_name, addr):
    output_road_name = extract_road_name(addr).lower()
    input_road_name = " ".join(road_name.lower().split()[:-1])
    return input_road_name == output_road_name


def process_road_points(snapped_points, road_name):
    if len(snapped_points) < 2:
        print("Nothing snapped")
        return []

    place_id = snapped_points[0].get("placeId")  # need a better way to select place id
    addr = get_address(place_id)
    if not is_correct_addr(road_name, addr):
        print("the place of chosen place ID doesn't match inputted road")

    location = snapped_points[0].get("location")
    road_coordinates = []
    road_coordinates.append([location.get("latitude"), location.get("longitude")])

    for i in range(1, len(snapped_points)):
        if snapped_points[i].get("placeId") == place_id:
            location = snapped_points[i].get("location")
            road_coordinates.append(
                [location.get("latitude"), location.get("longitude")]
            )

    return road_coordinates


def determine_street_orientation(road_coordinates):
    if len(road_coordinates) < 2:
        print("No coordinate in the street")
        return "Undeterminable"

    latitudes = [coord[0] for coord in road_coordinates]
    longitudes = [coord[1] for coord in road_coordinates]

    max_lat = max(latitudes)
    min_lat = min(latitudes)
    max_long = max(longitudes)
    min_long = min(longitudes)

    return "N/S" if abs(max_lat - min_lat) > abs(max_long - min_long) else "E/W"


def main():
    WKTs = [row[0] for row in data]
    road_names = [row[1] for row in data]
    proc_road_names = process_road_names(road_names)

    ## this is the real section (be careful and don't enable it or you'll incur fees)
    # for i in range(len(WKTs)):
    # i = 1
    # latitude, longitude = process_WKT(WKTs[i])
    # path = make_coordinates(latitude, longitude)
    # # print("path", path)
    # points = get_snap_to_roads(path)
    # # print("points", points)
    # coordinates = process_road_points(points, proc_road_names[i])
    # # print("coordinates", coordinates)
    # orientation = determine_street_orientation(coordinates)
    # print(orientation, latitude, longitude, proc_road_names[i])
    
    addrs = [
        "207 Bethells Road, Auckland 0781, New Zealand",
        "Unnamed Road, Te Henga (Bethells Beach) 0781, New Zealand",
        "4-70 Whatipu Road, Huia, Auckland 0604, New Zealand",
        "12-14 Seaview Road, Piha 0772, New Zealand",
        "Piha Road, Waiatarua, Auckland 0604, New Zealand",
        "60-96 Karekare Road, Auckland 0772, New Zealand",
        "4-20 Sylvan Glade, Piha 0772, New Zealand",
        "265 Glenbrook Beach Road, Glenbrook 2681, New Zealand",
        "218-252 Clevedon-Kawakawa Road, Clevedon 2585, New Zealand",
        "Waikopua Road, Whitford 2571, New Zealand",
        "Whitford-Maraetai Road, Whitford 2571, New Zealand",
        "10-22 Eastern Beach Road, Eastern Beach, Auckland 2012, New Zealand",
        "245-235 Bucklands Beach Road, Bucklands Beach, Auckland 2012, New Zealand",
    ]
    for i in range(len(proc_road_names)):
        print(is_correct_addr(proc_road_names[i], addrs[i]), proc_road_names[i], addrs[i])


if __name__ == "__main__":
    main()
