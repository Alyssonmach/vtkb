from geo_coords import coords_analysis

data = coords_analysis()
utm_test = {'south': 
            {'longitude': -46.6333, 'latitude': -23.5505, 'zone': 23, 'hemisphere': 'south'}, 
            'north': 
            {'longitude': -74.0060, 'latitude': 40.7128, 'zone': 18, 'hemisphere': 'north'}
            }

#############################

utm_crs_south = data.get_utm_zone(utm_test['south']['latitude'], utm_test['south']['longitude'])
utm_crs_north = data.get_utm_zone(utm_test['north']['latitude'], utm_test['north']['longitude'])

print(f'Teste de zonas UTM: \n\tSul: {utm_crs_south}\n\tNorte: {utm_crs_north}\n\n')

#############################

utm_x_south, utm_y_south = data.get_coords_utm(utm_test['south']['latitude'], utm_test['south']['longitude'])
utm_x_north, utm_y_north = data.get_coords_utm(utm_test['north']['latitude'], utm_test['north']['longitude'])

print(f"Coordenadas UTM Sul: X={utm_x_south:.2f}, Y={utm_y_south:.2f}")
print(f"Coordenadas UTM Norte: X={utm_x_north:.2f}, Y={utm_y_north:.2f}\n\n")

#############################

lat_south, long_south = data.utm_to_latlon(utm_x = utm_x_south, utm_y = utm_y_south, 
                                           zone = utm_test['south']['zone'], 
                                           hemisphere = utm_test['south']['hemisphere'])
lat_north, long_north = data.utm_to_latlon(utm_x = utm_x_north, utm_y = utm_y_north, 
                                           zone = utm_test['north']['zone'], 
                                           hemisphere = utm_test['north']['hemisphere'])

print('Conversão de UTM para latlon:')
print(f'Sul - Dados Originais: {utm_test['south']['latitude'], utm_test['south']['longitude']}')
print(f'Sul - Dados Reconvertidos: {lat_south, long_south}')
print(f'Norte - Dados Originais: {utm_test['north']['latitude'], utm_test['north']['longitude']}')
print(f'Norte - Dados Reconvertidos: {lat_north, long_north}')

############################

taq_torres = {'Torre1': 
                   {'lat': -19.9317348003, 'lon': -43.8526956561},
                   'Torre2':
                   {'lat': -19.9323032926, 'lon': -43.8536780703}}
distance = data.geodesic_distance_latlon(coords1 = (taq_torres['Torre1']['lat'], taq_torres['Torre1']['lon']),
                                         coords2 = (taq_torres['Torre2']['lat'], taq_torres['Torre2']['lon']))

p1_x_utm, p1_y_utm = data.get_coords_utm(latitude = taq_torres['Torre1']['lat'], 
                                         longitude = taq_torres['Torre1']['lon'])
p2_x_utm, p2_y_utm = data.get_coords_utm(latitude = taq_torres['Torre2']['lat'], 
                                         longitude = taq_torres['Torre2']['lon'])

distance_utm = data.utm_distance_same_zone(coords1 = (p1_x_utm, p1_y_utm), 
                                           coords2 = (p2_x_utm, p2_y_utm))

print('Distância entre pontos:')
print('\tDados de referência: ~120 metros - Torres perto da subestação de Taquaril')
print(f'\tDistância mensurada por latlon: {round(distance, 2)} metros')
print(f'\tDistância mensurada por utm: {round(distance_utm, 2)} metros')


