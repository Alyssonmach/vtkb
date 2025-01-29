from pyproj import CRS, Transformer

longitude = -46.6333
latitude = -23.5505
# longitude = -74.0060  # Nova York
# latitude = 40.7128   # Hemisfério Norte

utm_crs = CRS.from_user_input(f"+proj=utm +zone={int((longitude + 180) / 6) + 1} {'+south' if latitude < 0 else ''}")
print(utm_crs)

transformer = Transformer.from_crs("EPSG:4326", utm_crs, always_xy=True)

# Convertendo as coordenadas
utm_x, utm_y = transformer.transform(longitude, latitude)

print(f"Coordenadas UTM: X={utm_x:.2f}, Y={utm_y:.2f}")

