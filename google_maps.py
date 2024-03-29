import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("GOOGLE_API_KEY")
COOR_DIFF = 0.00009 * 2.5  # 10m * n

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

# This function processes the input WKT into usable latitude and longitude
def process_WKT(WKT):
    coordinate = WKT.strip("POINT ()").split()
    latitude = float(coordinate[1])
    longitude = float(coordinate[0])
    return latitude, longitude


def process_road_name(road_name):
    index_rd = road_name.find(" RD")
    index_st = road_name.find(" ST")
    index = max(index_rd, index_st)
    if index != -1:
        return road_name[:index]
    else:
        return road_name


# For using Roads API, you can input up to 100 coordinates and return the most likely roads the vehicle was traveling along.
# I add 8 additional coordinates that are 25 and 50 meters north/south/east/west from the coordinate on top of the coordinate. (refer: https://docs.google.com/document/d/1PBoyXQrwg7J-BmAyTV24JLppvIy9IkExPYvGwwjSLNs/edit?usp=sharing)
def make_coordinates(latitude, longitude):
    # 25m and 50m
    north = [latitude + COOR_DIFF, longitude]
    south = [latitude - COOR_DIFF, longitude]
    east = [latitude, longitude + COOR_DIFF]
    west = [latitude, longitude - COOR_DIFF]
    north_north = [latitude + COOR_DIFF * 2, longitude]
    south_south = [latitude - COOR_DIFF * 2, longitude]
    east_east = [latitude, longitude + COOR_DIFF * 2]
    west_west = [latitude, longitude - COOR_DIFF * 2]

    # This string gets attached to the HTTP request as one of params
    return f"{latitude}%2C{longitude}%7C{north[0]}%2C{north[1]}%7C{south[0]}%2C{south[1]}%7C{east[0]}%2C{east[1]}%7C{west[0]}%2C{west[1]}%7C{north_north[0]}%2C{north_north[1]}%7C{south_south[0]}%2C{south_south[1]}%7C{east_east[0]}%2C{east_east[1]}%7C{west_west[0]}%2C{west_west[1]}"


def get_snap_to_roads(path):
    endpoint = "https://roads.googleapis.com/v1/snapToRoads"
    params = {"interpolate": "true", "key": API_key, "path": path}
    url = endpoint + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        snapped_points = data.get("snappedPoints")
        if len(snapped_points) < 2:
            print("Nothing snapped")
            return []
        else:
            return snapped_points
    else:
        print("Error:", response.status_code)
        return []


def find_place_id(snapped_points, road_name):
    my_dict = {}
    for snapped_point in snapped_points:
        pid = snapped_point.get("placeId")
        my_dict[pid] = my_dict.get(pid, 0) + 1

    sorted_dict = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)
    for place_id, _ in sorted_dict:
        addr = get_address(place_id)
        print(place_id, addr)
        if is_correct_addr(road_name, addr):
            return place_id

    print("the place of chosen place ID doesn't match inputted road")
    return None


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


def is_correct_addr(road_name, addr):
    addrs_road_name = extract_road_name(addr)
    return addrs_road_name == road_name.lower()


def extract_road_name(address):
    addr_array = address.lower().split()
    if bool(re.search(r"\d", addr_array[0])):
        addr_array = addr_array[1:]

    result = []
    for element in addr_array:
        if "," in element:
            if "road" not in element and "street" not in element:
                result.append(element[:-1])
            break
        result.append(element)

    return " ".join(result).lower()


# From the Roads API output, filter out the coordinates that are not in the street provided
def process_road_points(snapped_points, place_id):
    if place_id is None:
        return []
    
    road_coordinates = []
    for snapped_point in snapped_points:
        if snapped_point.get("placeId") == place_id:
            location = snapped_point.get("location")
            road_coordinates.append(
                [location.get("latitude"), location.get("longitude")]
            )

    return road_coordinates


def determine_street_orientation(road_coordinates):
    if len(road_coordinates) < 2:
        print("Not enough coordinates in the street")
        return "Undeterminable"
    
    latitudes = [coord[0] for coord in road_coordinates]
    longitudes = [coord[1] for coord in road_coordinates]

    lat_dif = abs(max(latitudes) - min(latitudes))
    long_dif = abs(max(longitudes) - min(longitudes))

    if lat_dif == 0 and long_dif == 0:
        print("Not enough distance between coordinates")
        return "Undeterminable"
    return "N/S" if lat_dif > long_dif else "E/W"


def main():
    WKTs = [row[0] for row in data]
    road_names = [row[1] for row in data]

    ## this is the real section (be careful and don't enable it or you'll incur fees)
    for i in range(len(WKTs)):
        latitude, longitude = process_WKT(WKTs[i])
        proc_road_name = process_road_name(road_names[i])
        path = make_coordinates(latitude, longitude)
        # print("path", path)
        points = get_snap_to_roads(path)
        # print("points", points)
        place_id = find_place_id(points, proc_road_name)
        # print("place_id", place_id)
        coordinates = process_road_points(points, place_id)
        # print("coordinates", coordinates)
        orientation = determine_street_orientation(coordinates)
        print(i, orientation, road_names[i])


if __name__ == "__main__":
    main()
