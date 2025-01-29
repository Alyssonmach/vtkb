from pyproj import Transformer, CRS
from geopy.distance import geodesic
import requests
import math

class coords_analysis:
    '''
    Classe de manipulação de coordenadas geoespaciais.
    '''

    def __init__(self):
        '''
        Construtor da classe.

        Args:
            None
        
        Returns:
            None
        '''

        pass

    def get_utm_zone(self, latitude, longitude):
        '''
        Retorna a zona UTM e uma especificação caso esteja no hemisfério sul.

        Args:
            latitude (float): Coordenada precisa da latitude.
            longitude (float): Coordenada precisa da longitude.
        
        Returns:
            utm_crs (str): String no formato de especificação UTM do CRS.
        '''

        zone = int((longitude + 180) / 6) + 1
        hemisphere = '+south' if latitude < 0 else ''
        utm_crs = CRS.from_user_input(f"+proj=utm +zone={zone} {hemisphere}")

        return utm_crs

    def get_coords_utm(self, latitude, longitude, default_crs = 'EPSG:4326'):
        '''
        Obtenção das coordenadas no formato UTM.

        Args:
            latitude (float): Coordenada precisa da latitude.
            longitude (float): Coordenada precisa da longitude.
            default_crs (str): O CRS padrão para latitude e longitude em graus (`default = EPSG:4326`).
        
        Returns:
            utm_x (float): Retorna a coordenada cartesiana x em UTM.
            utm_y (float): Retorna a coordenada cartesiana y em UTM.
        '''

        utm_crs = self.get_utm_zone(latitude = latitude, longitude = longitude)
        transformer = Transformer.from_crs(default_crs, utm_crs, always_xy=True)
        utm_x, utm_y = transformer.transform(longitude, latitude)

        return utm_x, utm_y

    def utm_to_latlon(self, utm_x, utm_y, zone, hemisphere):
        '''
        Converte coordenadas UTM para coordenadas de latitude e longitude.

        Args:
            utm_x (float): Coordenada cartesiana x em UTM.
            utm_y (float): Coordenada cartesiana y em UTM.
            zone (int): Zona UTM da coordenadas.
            hemisphere (str): hemisfério onde está localizado (`south` ou `north`).
        Returns:
            latitude (float): Coordenada precisa da latitude.
            longitude (float): Coordenada precisa da longitude.
        '''

        epsg_code = 32600 + zone if hemisphere == 'north' else 32700 + zone
        utm_crs = CRS.from_epsg(epsg_code)
        wgs84_crs = CRS.from_epsg(4326)
        transformer = Transformer.from_crs(utm_crs, wgs84_crs, always_xy=True)
        longitude, latitude = transformer.transform(utm_x, utm_y)

        return latitude, longitude
    
    def geodesic_distance_latlon(self, coords1, coords2):
        '''
        Obtém a distância geodésica em metros a partir de coordenadas (latitude, longitude).

        Args:
            coords1 (list): Coordenada (lat, lon) do primeiro ponto.
            coords2 (list): Coordenada (lat, lon) do segundo ponto.
            is_same_zone (bool): Indica se os pontos pertencem a uma mesma zona UTM.
        
        returns:
            distance (float): Distância em metros dos dois pontos.
        '''

        distance = geodesic(coords1, coords2).meters
        
        zone1 = self.get_utm_zone(latitude = coords1[0], longitude = coords1[1])
        zone2 = self.get_utm_zone(latitude = coords2[0], longitude = coords2[1])

        is_same_zone = zone1 == zone2

        return distance, is_same_zone
    
    def utm_distance_same_zone(self, coords1, coords2):
        '''
        Obtém a distância euclidiana em metros a partir de coordenadas (latitude, longitude).

        Args:
            coords1 (list): Coordenada (utm_x, utm_y) do primeiro ponto.
            coords2 (list): Coordenada (utm_x, utm_y) do segundo ponto.
        
        returns:
            distance (float): Distância em metros dos dois pontos.
        '''

        x1, y1 = coords1
        x2, y2 = coords2

        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def get_altitude_ort(self, latitude, longitude):
        '''
        Retorna a altitude ortométrica baseado em coordenadas de latitude e longitude.

        Args:
            latitude (float): Coordenada precisa da latitude.
            longitude (float): Coordenada precisa da longitude.
        
        Returns:
            altitude (float): Altitude ortométrica para a coordenada de referência.
        '''
      
        url = f"https://api.opentopodata.org/v1/srtm30m?locations={latitude},{longitude}"
        response = requests.get(url)
        data = response.json()
        altitude = data['results'][0]['elevation']
        
        return altitude

    