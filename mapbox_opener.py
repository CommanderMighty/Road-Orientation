import webbrowser

chrome_path = '"C:\Program Files\Google\Chrome\Application\chrome.exe" %s' 

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

coordinates = []

def process_WKT(WKT):
    coordinate = WKT.strip("POINT ()").split()
    latitude = float(coordinate[1])
    longitude = float(coordinate[0])
    return latitude, longitude

def open_mapbox_on_chrome():
  for WKT in WKTs:
      latitude, longitude = process_WKT(WKT)
      url = f"http://127.0.0.1:5500/mapbox.html#20/{latitude}/{longitude}"
      
      webbrowser.get(chrome_path).open(url)


def open_google_maps_on_chrome(): 
  for coordinate in coordinates:
      url = f"http://maps.google.com/?ll={coordinate[0]},{coordinate[1]}"     
      webbrowser.get(chrome_path).open(url)
      
open_mapbox_on_chrome()
# open_google_maps_on_chrome()