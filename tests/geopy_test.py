from pyproj import Transformer, CRS
from geopy.distance import geodesic

def utm_to_latlong(utm_x, utm_y, zone, hemisphere='S'):
    # Define o EPSG baseado na zona e hemisfério
    epsg_code = 32600 + zone if hemisphere.upper() == 'N' else 32700 + zone
    utm_crs = CRS.from_epsg(epsg_code)
    wgs84_crs = CRS.from_epsg(4326)
    transformer = Transformer.from_crs(utm_crs, wgs84_crs, always_xy=True)
    longitude, latitude = transformer.transform(utm_x, utm_y)
    return latitude, longitude

# Pontos em UTM
point1 = (334742.01, 7390402.50)  # UTM (x, y)
zone1 = 23
hemisphere1 = 'S'

point2 = (500000.00, 7400000.00)  # UTM (x, y)
zone2 = 24
hemisphere2 = 'S'

# Converte para latitude/longitude
latlong1 = utm_to_latlong(*point1, zone1, hemisphere1)
latlong2 = utm_to_latlong(*point2, zone2, hemisphere2)

print(f'first point: {latlong1}')
print(f'second point: {latlong2}')

# Calcula a distância geodésica (em metros)
distance = geodesic(latlong1, latlong2).meters
print(f"Distância geodésica: {distance:.2f} metros")
