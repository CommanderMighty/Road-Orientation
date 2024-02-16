// index 0
var coordinates = [
    [-36.8860243241, 174.4513638653], [-36.8857993241, 174.4513638653], [-36.8862493241, 174.4513638653], [-36.8860243241, 174.4515888653], [-36.8860243241, 174.4511388653], [-36.8855743241, 174.4513638653], [-36.8864743241, 174.4513638653], [-36.8860243241, 174.4518138653], [-36.8860243241, 174.4509138653]
]
coordinates.forEach(coordinate => {
    L.marker(coordinate).addTo(map);
})


var points = [{ 'location': { 'latitude': -36.88602151841069, 'longitude': 174.45135707423856 }, 'originalIndex': 0, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }, { 'location': { 'latitude': -36.885990199999995, 'longitude': 174.4513773 }, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }, { 'location': { 'latitude': -36.885847137721285, 'longitude': 174.4514742050487 }, 'originalIndex': 1, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }, { 'location': { 'latitude': -36.8857658, 'longitude': 174.4515293 }, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }, { 'location': { 'latitude': -36.885639415424215, 'longitude': 174.4515869443197 }, 'originalIndex': 5, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }]
points.forEach(point => {
    let coordinate = [point.location.latitude, point.location.longitude]
    L.marker(coordinate).addTo(map);
})

// index 1

// index 6