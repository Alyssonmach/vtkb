import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

def main():
    st.title("Manipulação de Coordenadas - Trixel")
    st.write("Entre com as coordenadas de dois pontos para visualizar no mapa e calcular a distância.")

    # Inputs para as coordenadas
    col1, col2 = st.columns(2)

    with col1:
        lat1 = st.number_input("Latitude do Ponto 1", value=-19.9317348003, format="%.6f", key="lat1")
        lon1 = st.number_input("Longitude do Ponto 1", value=-43.8526956561, format="%.6f", key="lon1")

    with col2:
        lat2 = st.number_input("Latitude do Ponto 2", value=-19.9323032926, format="%.6f", key="lat2")
        lon2 = st.number_input("Longitude do Ponto 2", value=-43.8536780703, format="%.6f", key="lon2")

    # Botão para calcular e mostrar no mapa
    if st.button("Gerar Mapa"):
        # Salva os valores em session_state
        st.session_state["point1"] = (lat1, lon1)
        st.session_state["point2"] = (lat2, lon2)

    # Só gera o mapa se os pontos estiverem disponíveis no estado
    if "point1" in st.session_state and "point2" in st.session_state:
        point1 = st.session_state["point1"]
        point2 = st.session_state["point2"]

        # Calcula a distância entre os pontos
        distance = geodesic(point1, point2).meters
        st.write(f"Distância entre os pontos: {distance:.2f} metros")

        # Cria o mapa centrado entre os dois pontos
        map_center = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]
        m = folium.Map(location=map_center, zoom_start=12)

        # Adiciona os pontos no mapa
        folium.Marker(location=point1, popup="Ponto 1", icon=folium.Icon(color="blue")).add_to(m)
        folium.Marker(location=point2, popup="Ponto 2", icon=folium.Icon(color="green")).add_to(m)

        # Adiciona uma linha entre os dois pontos
        folium.PolyLine([point1, point2], color="red", weight=2.5, opacity=1).add_to(m)

        # Mostra o mapa
        st_folium(m, width=700, height=500)

if __name__ == "__main__":
    main()
