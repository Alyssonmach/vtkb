import streamlit as st
import folium
from streamlit_folium import st_folium
import elevation
import rasterio
import numpy as np
import pandas as pd
import plotly.express as px

# Função para obter elevação usando rasterio
def get_elevation(lat, lon):
    # Baixa os dados SRTM para a região
    elevation.clip(bounds=(lon - 0.1, lat - 0.1, lon + 0.1, lat + 0.1))
    tif_file = "elevation.tif"
    
    # Lê o arquivo .tif com rasterio
    with rasterio.open(tif_file) as src:
        # Converte coordenadas geográficas para índices no array raster
        row, col = src.index(lon, lat)
        elevation_value = src.read(1)[row, col]
    
    return elevation_value

# Configuração do Streamlit
st.title("Perfil Longitudinal - Dados SRTM")
st.write("Selecione dois pontos no mapa para calcular o perfil longitudinal com base na altitude (SRTM).")

# Configuração inicial do mapa
map_center = [-23.55052, -46.633308]  # Centro de São Paulo
map_ = folium.Map(location=map_center, zoom_start=12)

# Seleção de pontos no mapa
with st.expander("Selecione dois pontos no mapa"):
    ponto1 = st.text_input("Coordenadas do ponto 1 (lat, lon)", "-23.55052, -46.633308")
    ponto2 = st.text_input("Coordenadas do ponto 2 (lat, lon)", "-23.56134, -46.65442")
    
    if ponto1 and ponto2:
        lat1, lon1 = map(float, ponto1.split(","))
        lat2, lon2 = map(float, ponto2.split(","))
        
        folium.Marker([lat1, lon1], popup="Ponto 1").add_to(map_)
        folium.Marker([lat2, lon2], popup="Ponto 2").add_to(map_)
        folium.PolyLine([[lat1, lon1], [lat2, lon2]], color="blue").add_to(map_)

map_view = st_folium(map_, width=700)

# Cálculo do perfil longitudinal
if ponto1 and ponto2:
    lat1, lon1 = map(float, ponto1.split(","))
    lat2, lon2 = map(float, ponto2.split(","))
    
    # Obtendo as elevações dos pontos
    elevation1 = get_elevation(lat1, lon1)
    elevation2 = get_elevation(lat2, lon2)
    
    if elevation1 and elevation2:
        st.write(f"Elevação do Ponto 1: {elevation1:.2f} m")
        st.write(f"Elevação do Ponto 2: {elevation2:.2f} m")
        
        # Simulando dados de perfil longitudinal (interpolação)
        distances = np.linspace(0, 1, 100)
        elevations = np.linspace(elevation1, elevation2, 100)
        df = pd.DataFrame({"Distância (km)": distances, "Elevação (m)": elevations})
        
        # Plotando gráfico
        fig = px.line(df, x="Distância (km)", y="Elevação (m)", title="Perfil Longitudinal")
        st.plotly_chart(fig)
