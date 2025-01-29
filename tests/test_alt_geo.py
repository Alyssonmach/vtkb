import requests

def get_altitude(latitude, longitude):
    url = f"https://api.opentopodata.org/v1/srtm30m?locations={latitude},{longitude}"
    response = requests.get(url)
    data = response.json()
    altitude = data['results'][0]['elevation']
    return altitude

latitude, longitude = (-19.5967586922,-43.0338450992)

altitude = get_altitude(latitude, longitude)
print(f"Altitude ortométrica: {altitude} metros")