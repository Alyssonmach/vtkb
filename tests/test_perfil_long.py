import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Função para calcular a distância cumulativa entre as torres
def calcular_distancia_cumulativa(coordenadas):
    distancias = [0]  # A primeira torre tem distância cumulativa zero
    for i in range(1, len(coordenadas)):
        # Calcula a distância entre a torre atual e a anterior usando geodesic
        distancia = geodesic(coordenadas[i-1], coordenadas[i]).meters
        distancias.append(distancias[i-1] + distancia)
    return distancias

# Dados de exemplo (substitua pelos seus dados)
dados = {
    "Torre": ["Torre 1", "Torre 2", "Torre 3", "Torre 4"],
    "Latitude": [-22.9068, -23.5505, -24.0059, -25.4296],
    "Longitude": [-43.1729, -46.6333, -46.4253, -49.2719],
    "Altitude (m)": [10, 50, 120, 80]
}

# Criar DataFrame
df = pd.DataFrame(dados)

# Calcular distância cumulativa
coordenadas = list(zip(df["Latitude"], df["Longitude"]))
df["Distância Cumulativa (m)"] = calcular_distancia_cumulativa(coordenadas)

# Interface do Streamlit
st.title("Perfil Longitudinal das Torres de Transmissão")
st.write("Gráfico de altitude ortométrica em função da distância cumulativa.")

# Plotar o gráfico
fig, ax = plt.subplots()
ax.plot(df["Distância Cumulativa (m)"], df["Altitude (m)"], marker='o', linestyle='-', color='b')
ax.set_xlabel("Distância Cumulativa (m)")
ax.set_ylabel("Altitude Ortométrica (m)")
ax.set_title("Perfil Longitudinal")
ax.grid(True)

# Exibir o gráfico no Streamlit
st.pyplot(fig)

# Exibir tabela de dados
st.write("Dados das Torres:")
st.dataframe(df)