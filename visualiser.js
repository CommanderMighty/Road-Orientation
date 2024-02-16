// index 0
var coordinates = [
    [-36.8860243241, 174.4513638653], [-36.8857993241, 174.4513638653], [-36.8862493241, 174.4513638653], [-36.8860243241, 174.4515888653], [-36.8860243241, 174.4511388653], [-36.8855743241, 174.4513638653], [-36.8864743241, 174.4513638653], [-36.8860243241, 174.4518138653], [-36.8860243241, 174.4509138653]
]
coordinates.forEach(coordinate => L.marker(coordinate).addTo(map))


var points = [{ 'location': { 'latitude': -36.88602151841069, 'longitude': 174.45135707423856 }, 'originalIndex': 0, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }, { 'location': { 'latitude': -36.885990199999995, 'longitude': 174.4513773 }, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }, { 'location': { 'latitude': -36.885847137721285, 'longitude': 174.4514742050487 }, 'originalIndex': 1, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }, { 'location': { 'latitude': -36.8857658, 'longitude': 174.4515293 }, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }, { 'location': { 'latitude': -36.885639415424215, 'longitude': 174.4515869443197 }, 'originalIndex': 5, 'placeId': 'ChIJhTU6VpJtDW0RHa85MAgdzc0' }]
points.forEach(point => {
    let coordinate = [point.location.latitude, point.location.longitude]
    L.marker(coordinate).addTo(map);
})

// index 1
var str = "-36.8913620998%2C174.4497720357%7C-36.8911370998%2C174.4497720357%7C-36.8915870998%2C174.4497720357%7C-36.8913620998%2C174.4499970357%7C-36.8913620998%2C174.4495470357%7C-36.8909120998%2C174.4497720357%7C-36.8918120998%2C174.4497720357%7C-36.8913620998%2C174.4502220357%7C-36.8913620998%2C174.4493220357"
var coordinates = parseCoordinates(str)
coordinates.forEach(coordinate => L.marker(coordinate).addTo(map))

var points = [{ 'location': { 'latitude': -36.89126949443993, 'longitude': 174.44992497692377 }, 'originalIndex': 0, 'placeId': 'ChIJwU2bDO1tDW0RnnP0mk-Nhec' }, { 'location': { 'latitude': -36.8912036, 'longitude': 174.4498626 }, 'originalIndex': 1, 'placeId': 'ChIJwU2bDO1tDW0RnnP0mk-Nhec' }, { 'location': { 'latitude': -36.8912036, 'longitude': 174.4498626 }, 'placeId': 'ChIJJc0Deu1tDW0RCattoQ47kwM' }, { 'location': { 'latitude': -36.891375920932035, 'longitude': 174.44957453679012 }, 'originalIndex': 2, 'placeId': 'ChIJJc0Deu1tDW0RCattoQ47kwM' }, { 'location': { 'latitude': -36.89138151200802, 'longitude': 174.44956519033184 }, 'originalIndex': 4, 'placeId': 'ChIJJc0Deu1tDW0RCattoQ47kwM' }, { 'location': { 'latitude': -36.891423499999995, 'longitude': 174.44949499999998 }, 'placeId': 'ChIJJc0Deu1tDW0RCattoQ47kwM' }, { 'location': { 'latitude': -36.891469521946995, 'longitude': 174.449424147918 }, 'originalIndex': 6, 'placeId': 'ChIJJc0Deu1tDW0RCattoQ47kwM' }]
points.forEach(point => {
    let coordinate = [point.location.latitude, point.location.longitude]
    L.marker(coordinate).addTo(map);
})

// index 6
var str = ""
var coordinates = parseCoordinates(str)
coordinates.forEach(coordinate => L.marker(coordinate).addTo(map))

var points = []
