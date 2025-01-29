from pyproj import Transformer, CRS

# Coordenadas de entrada (latitude e longitude)
latitude = -23.5505  # Latitude de São Paulo
longitude = -46.6333  # Longitude de São Paulo

# Definindo a projeção geográfica (WGS84) e a projeção UTM (automática para a posição)
utm_zone = CRS.from_epsg(32723) if latitude < 0 else CRS.from_epsg(32623)  # Zona 23S para SP
transformer = Transformer.from_crs("EPSG:4326", utm_zone, always_xy=True)

# Convertendo as coordenadas
utm_x, utm_y = transformer.transform(longitude, latitude)
print(f'utm zone: {utm_zone}')
print(f"Coordenadas UTM: X={utm_x:.2f}, Y={utm_y:.2f}")
