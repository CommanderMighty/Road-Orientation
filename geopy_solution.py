import math
from geopy.geocoders import Nominatim

DISTANCE = 100 * 0.000009 
geolocator = Nominatim(user_agent="street_orientation_app")

WKTs = [
  "POINT (174.4513638653 -36.8860243241)",
  "POINT (174.4497720357 -36.8913620998)",
  "POINT (174.556297882 -37.0165364501)",
  "POINT (174.4712833983 -36.9534253801)",
  "POINT (174.5438302975 -36.9442337643)",
  "POINT (174.4801522996 -36.9775084447)",
  "POINT (174.4699737384 -36.9573123506)",
  "POINT (174.7312755423 -37.1828783774)",
  "POINT (175.056786306 -36.9781819942)",
  "POINT (175.000106141 -36.9285970881)",
  "POINT (174.9726129099 -36.9410602158)",
  "POINT (174.9097212116 -36.871404902)",
  "POINT (174.9110686595 -36.8818525921)",
]

road_names = [
  "BETHELLS RD (WCC)",
  "BETHELLS RD (WCC)",
  "WHATIPU RD",
  "SEAVIEW RD (PIHA)",
  "PIHA RD",
  "KAREKARE RD",
  "BEACH VALLEY RD",
  "GLENBROOK BEACH RD",
  "CLEVEDON-KAWAKAWA RD",
  "WAIKOPUA RD",
  "WHITFORD-MARAETAI RD",
  "EASTERN BEACH RD",
  "BUCKLANDS BEACH RD",
]

directions = [
    # [direction, latitude, longitude]
    ['NN', DISTANCE, 0], 
    ['NNE', math.sin(math.pi / 3) * DISTANCE, math.cos(math.pi / 3) * DISTANCE], 
    ['NEE', math.cos(math.pi / 3) * DISTANCE, math.sin(math.pi / 3) * DISTANCE], 
    ['EE', 0, DISTANCE], 
    ['SEE', math.cos(math.pi / 3) * -DISTANCE, math.sin(math.pi / 3) * DISTANCE], 
    ['SSE', math.sin(math.pi / 3) * -DISTANCE, math.cos(math.pi / 3) * DISTANCE], 
    ['SS', -DISTANCE, 0], 
    ['SSW', math.sin(math.pi / 3) * -DISTANCE, math.cos(math.pi / 3) * -DISTANCE], 
    ['SWW', math.cos(math.pi / 3) * -DISTANCE, math.sin(math.pi / 3) * -DISTANCE], 
    ['WW', 0, -DISTANCE], 
    ['NWW', math.cos(math.pi / 3) * DISTANCE, math.sin(math.pi / 3) * -DISTANCE],  
    ['NNW', math.sin(math.pi / 3) * DISTANCE, math.cos(math.pi / 3) * -DISTANCE], 
]

def process_road_names(road_names):
    processed_road_names = []
    for name in road_names:
        index_rd = name.find(" RD")
        index_st = name.find(" ST")
        index = max(index_rd, index_st)
        if index != -1:
            processed_road_names.append(name[:index + 3])
        else:
            processed_road_names.append(name)
    return processed_road_names

def process_WKT(WKT):
    coordinate = WKT.strip("POINT ()").split()
    latitude = float(coordinate[1])
    longitude = float(coordinate[0])
    return latitude, longitude

def trim_road_name(road_name):
    return "".join(road_name.lower().split()[:-1])

def get_street_orientation(latitude, longitude, road_name):
    dirs = ['NN','NNE','NEE','EE','SEE','SSE','SS', 'SSW','SWW','WW', 'NWW','NNW']
    name = trim_road_name(road_name)
    
    cur_location = geolocator.reverse((latitude, longitude), language='en')
    # print('1', latitude, longitude)
    # print('2', cur_location.latitude, cur_location.longitude)
    # print(abs(latitude - cur_location.latitude) / abs(longitude - cur_location.longitude))
    # print("N/S" if abs(latitude - cur_location.latitude) > abs(longitude - cur_location.longitude) else "E/W")
    
    cur_road_name = cur_location.raw.get('address', {}).get('road', '')
    cur_name = trim_road_name(cur_road_name)

    if name != cur_name:
        print("something is wrong", road_name, cur_road_name, cur_location)
        return ""
        # the coordinate's road name doesn't match the datasheet's road name, 
        # something needs to be handled

    # x = 1
    # while x <= 10 and len(dirs) > 1:
    #     for direction in directions: 
    #         if direction[0] not in dirs:
    #             continue
            
    #         new_lat = latitude + direction[1] * x
    #         new_long = longitude + direction[2] * x
    #         # print(f"{direction[0]} {new_lat}/{new_long}")
            
    #         cur_location = geolocator.reverse((new_lat, new_long), language='en')
    #         cur_road_name = cur_location.raw.get('address', {}).get('road', '')
    #         cur_name = trim_road_name(cur_road_name)
    #         if cur_name != name:
    #             print(direction[0], f"{new_lat}/{new_long}")
    #             dirs.remove(direction[0])
    #             if len(dirs) == 1:
    #                 break
    #             # print(f"{direction[0]}, {cur_road_name}")
    #     x += 1 
    
    if len(dirs) != 1:
        return "undetermined"
    else:
        return get_east_or_south(dirs[0])
    
def get_east_or_south(direction):
    print("final direction", direction)
    if "EE" in direction or "WW" in direction:
        return "E/W"
    else:         
        return "N/S"

def main():    
    processed_road_names = process_road_names(road_names)
    
    for i in range(len(WKTs)):
    # i = 0
        latitude, longitude = process_WKT(WKTs[i])
        orientation = get_street_orientation(latitude, longitude, processed_road_names[i])
        print()
        # print(i, orientation)

if __name__ == '__main__':
    main()