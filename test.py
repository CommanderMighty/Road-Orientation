COOR_DIFF = 0.00009 * 5 # 10m * n

jsonData = {
    "snappedPoints": [
        {
            "location": {
                "latitude": -36.886021518410693,
                "longitude": 174.45135707423856
            },
            "originalIndex": 0,
            "placeId": "ChIJhTU6VpJtDW0RHa85MAgdzc0"
        },
        {
            "location": {
                "latitude": -36.885990199999995,
                "longitude": 174.4513773
            },
            "placeId": "ChIJhTU6VpJtDW0RHa85MAgdzc0"
        },
        {
            "location": {
                "latitude": -36.8857658,
                "longitude": 174.4515293
            },
            "placeId": "ChIJhTU6VpJtDW0RHa85MAgdzc0"
        },
        {
            "location": {
                "latitude": -36.885639415424215,
                "longitude": 174.4515869443197
            },
            "originalIndex": 1,
            "placeId": "ChIJhTU6VpJtDW0RHa85MAgdzc0"
        }
    ]
}

def add_to_coordinate(coordinates):
    [latitude, longitude] = coordinates
    north = [latitude + COOR_DIFF, longitude]
    south = [latitude - COOR_DIFF, longitude]
    east = [latitude, longitude + COOR_DIFF]
    west = [latitude, longitude - COOR_DIFF]
    print(f"{coordinates[0]} {coordinates[1]}")
    print(f"{north[0]} {north[1]}")
    print(f"{south[0]} {south[1]}")
    print(f"{east[0]} {east[1]}")
    print(f"{west[0]} {west[1]}")
    print(f"{coordinates[0]}%2C{coordinates[1]}%7C{north[0]}%2C{north[1]}%7C{south[0]}%2C{south[1]}%7C{east[0]}%2C{east[1]}%7C{west[0]}%2C{west[1]}")

def process_road_points():
    
    snapped_points = jsonData.get('snappedPoints')

    place_id = snapped_points[0].get('placeId')
    location = snapped_points[0].get('location')
    coordinates = []
    coordinates.append([location.get('latitude'), location.get('longitude')])

    for i in range(1, len(snapped_points)):
        if snapped_points[i].get('placeId') == place_id:
            location = snapped_points[i].get('location')
            coordinates.append([location.get('latitude'), location.get('longitude')])
        else: 
            print("Wrong Street")
        
    return coordinates
        
def determine_street_orientation(road_coordinates):
    latitudes = [coord[0] for coord in road_coordinates]
    longitudes = [coord[1] for coord in road_coordinates]
    
    # Find max and min values
    max_lat = max(latitudes)
    min_lat = min(latitudes)
    max_long = max(longitudes)
    min_long = min(longitudes)
    
    return "N/S" if abs(max_lat - min_lat) > abs(max_long - min_long) else "E/W"
    
# add_to_coordinate([-36.8860243241, 174.4513638653]) 
road_coordinates = process_road_points()
print(road_coordinates)
street_orientation = determine_street_orientation(road_coordinates)
print(street_orientation)