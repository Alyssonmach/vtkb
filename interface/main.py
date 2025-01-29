from data_manipulation import render_data
from matplotlib import pyplot as plt
from geo_coords import coords_analysis
import plotly.graph_objects as go
import streamlit as st
from math import isnan
import pandas as pd
import simplekml
import folium
import paths
import ezdxf
import os

# Configurações da visualização da página
st.set_page_config(
    page_title='Trixel - SW Torres',
    page_icon='⚡')

# Módulos para renderização dos dados na interface
data_modules = render_data()
# Módulos para estimação de distância de coordenadas
geo_conversor = coords_analysis()

# Caminhos das tabelas e colunas de referência para acesso dos dados do GEO BDIT
df_paths = paths.return_data_paths(yaml_file = 'config.yaml')
columns_names = paths.return_columns_ref(yaml_file = 'config.yaml')

def folium_map_data(label):
    '''
    Renderiza torres e distâncias de vãos por conjuntos de vãos.

    Args:
        label (str): Atributo com o nome do conjunto de linha.
    
    Returns:
        m (folium object): Objeto com os atributos de renderização do mapa no Folium.
        value_towers (dict): Dicionário com os dados das estruturas do conjunto.
        values_conexions (dict): Dicionário com os dados das conexões entre estruturas do conjunto.
        coords (dict): Informações sobre as torres de transmissão. 
        zone_utm_problem (bool): Indica se há problemas de diferentes zonas UTM.
    '''
    
    # Variável para verificar se há mudanças de zona UTM
    zone_utm_problem = False

    values_towers, coords, values_conexions = data_modules.separate_conj_data(df_paths = df_paths, columns_names = columns_names, label = label) 

    # Configurando o exportador do projeto para kml
    kml = simplekml.Kml()

    # Configura a visualização do mapa via frame do folium
    center = len(coords) // 2
    map_center = (coords[center]['lat'], coords[center]['long'])
    m = folium.Map(location = map_center, zoom_start = 12)

    # Adicionando a visualização com imagem de satélite
    folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite',
    overlay=True).add_to(m)

    # Adiciona as estruturas do conjunto de linhas no mapa
    for coord in coords:
        popup_text = f'''
        <b>Cod. Torre</b>: {coord['structure']}<br>
        <b>ID</b>: {coord['num_id']}<br>
        <b>Tipo</b>: {coord['est_type']}<br>
        <b>Altura</b>: {coord['val_alt']} <br>
        <b>Caracter. 1</b>: {coord['character1']}<br>
        <b>Caracter. 2</b>:  {coord['character2']}<br>
        <b>Alt. Ortométrica</b>: {coord['alt_ort']}
        '''

        folium.Marker(location = (coord['lat'], coord['long']), popup = folium.Popup(popup_text, max_width = 300), 
                    icon=folium.Icon(color = 'green')).add_to(m)
        
        # Adicionando as informações ao exportador do projeto para .kml
        pnt = kml.newpoint(name = coord['num_id'], coords = [(coord['long'], coord['lat'])])  # KML usa (lon, lat)
        pnt.description = popup_text
    
    # Adiciona as conexões entre vãos e a mensuração de distância entre as torres
    for conexion in values_conexions:
        try:
            coord1 = [conexion['NUM_LATITUDE_ESTRUTURA_INI'], conexion['NUM_LONGITUDE_ESTRUTURA_INI']]
            name1 = conexion['COD_ESTRUTURA_INI_SAP']
            coord2 = [conexion['NUM_LATITUDE_ESTRUTURA_FIM'], conexion['NUM_LONGITUDE_ESTRUTURA_FIM']]
            name2 = conexion['COD_ESTRUTURA_FIM_SAP']
            
            # Caso não tenha as coordenadas dos vãos, recompor os dados pela coordenadas das estruturas
            is_nan = any(isnan(item) for subcoord in [coord1, coord2] for item in subcoord)
            if is_nan: 
                data1 = [element for element in coords if element['structure'] == conexion['COD_ESTRUTURA_INI_SAP']]
                coord1 = (data1[0]['lat'], data1[0]['long'])
                data2 = [element for element in coords if element['structure'] == conexion['COD_ESTRUTURA_FIM_SAP']]
                coord2 = (data2[0]['lat'], data2[0]['long']) 

            # Calcula a distância geodésica dos vãos
            distance_latlon, is_same_zone = geo_conversor.geodesic_distance_latlon(coord1, coord2)

            # Informe se há mudança de zona nas coordenadas UTM
            if is_same_zone:
                # Calcula a distância por coordenadas UTM
                utm1_x, utm1_y = geo_conversor.get_coords_utm(coord1[0], coord1[1])
                utm2_x, utm2_y = geo_conversor.get_coords_utm(coord2[0], coord2[1])
                distance_utm = geo_conversor.utm_distance_same_zone((utm1_x, utm1_y), (utm2_x, utm2_y))
            else: 
                # Adiciona a distância geodésica caso a distância por coordenadas UTM não seja válida
                zone_utm_problem = True
                distance_utm = distance_latlon

            popup_text = f'''
            <b>{conexion['COD_ESTRUTURA_INI_SAP']}</b> e <b>{conexion['COD_ESTRUTURA_FIM_SAP']}</b><br>
            <b>Dist. Geodésica</b>: {round(distance_latlon, 2)} m<br>
            <b>Dist. UTM</b>: {round(distance_utm, 2)} m
            '''
            
            folium.PolyLine([coord1, coord2], color = "red", weight = 4, opacity = 1,
                            popup = folium.Popup(popup_text, max_width = 300)).add_to(m)
            
            # exportando os dados para o projeto em .kml
            line = kml.newlinestring(
                coords=[
                    (coord1[1], coord1[0]),  # KML usa (lon, lat)
                    (coord2[1], coord2[0]),
                ]
            )
            line.name = f'{name1} | {name2}',
            line.description = popup_text

        except Exception as e:
            print(f'Erro ao renderizar: {e}')
    
    kml_file = f'out_data/{label}.kml'
    kml.save(kml_file)
    
    return m, values_towers, values_conexions, coords, zone_utm_problem

def get_df_template():
    '''
    Retorna um template dos atributos da tabela com as informações gerais.

    Args:
        None
    
    Returns:
        data (dict): Dicionário com o template dos atributos de cada elemento da tabela.
    '''

    data = {'EST1_SAP': '', 'EST1_ALT_ORT': '', 'EST1_LAT': '', 'EST1_LON': '', 'EST1_UTM_X': '', 'EST1_UTM_Y': '',
            'EST1_ID': '', 'EST1_ALTURA': '', 'EST1_TIPO': '', 'EST1_CARACT1': '', 'EST1_CARACT2': '',
            'EST2_SAP': '', 'EST2_ALT_ORT': '', 'EST2_LAT': '', 'EST2_LON': '', 'EST2_UTM_X': '', 'EST2_UTM_Y': '',
            'EST2_ID': '', 'EST2_ALTURA': '', 'EST2_TIPO': '', 'EST2_CARACT1': '', 'EST2_CARACT2': '',
            'NOME_LT': '', 'SAP_LT': '', 'DIS_M': '', 'VAO_CENTRO_LAT': '', 'VAO_CENTRO_LONG': '', 'VAO_CENTRO_ALT_ORT': ''}
    
    return data

def reorganize_csv(df):
    '''
    Reorganiza o dataframe para as linhas ficarem em ordem com as conexões.

    Args:
        df (dataframe): Dataframe pandas sem ordenação de conexões entre as linhas.
    
    Returns:
        df (dataframe): Dataframe pandas com ordenação de conexões entre as linhas.
    '''

    # Identificar a linha inicial (primeiro port alfabeticamente)
    df = df.sort_values(by=["EST1_SAP"]) 
    start_row = df[df["EST1_SAP"].str.startswith("PORT")].iloc[0]
    current_link = start_row["EST2_SAP"]

    # Criar nova ordem
    ordered_rows = [start_row]
    while True:
        # Buscar a próxima linha
        next_row = df[df["EST1_SAP"] == current_link]
         # Se não há mais conexões, encerra
        if next_row.empty:
            break 
        # Seleciona a primeira correspondência
        next_row = next_row.iloc[0]  
        ordered_rows.append(next_row)
        current_link = next_row["EST2_SAP"]

    # Criar o novo dataframe reordenado
    new_df = pd.DataFrame(ordered_rows)

    return new_df

def make_dataset(label, values_towers, values_conexions, coords_towers):
    '''
    Agrupa os dados do conjunto de linhas em uma tabela estruturada.

    Args:
        label (str): Rótulo da linha.
        values_towers (dataframe): Dataframe das estruturas.
        values_conexions (dataframe): Dataframe dos vãos entre estruturas.
        coords_towers (dict): Informações sobre as torres de transmissão. 
    
    Returns:
        df (dataframe): Dataframe estruturado dos conjuntos de linhas.
        df_integrity (bool): Informa se todos os dados foram coletados.
    '''

    # Variável para monitorar a integridade do dataset
    df_integrity = True

    geo_conversor = coords_analysis()
    all_data = list()

     # Agrupamento dos dados
    for conexion in values_conexions:
        data = get_df_template()
        coords = list()

        for i in range(1,3):
            ref = 'INI' if i == 1 else 'FIM' 

            data[f'EST{i}_SAP'] = conexion[f'COD_ESTRUTURA_{ref}_SAP']
            data[f'EST{i}_ALT_ORT'] = conexion[f'NUM_ALTITUDE_ORT_ESTRUTURA_{ref}']
            data[f'EST{i}_LAT'] = conexion[f'NUM_LATITUDE_ESTRUTURA_{ref}']
            data[f'EST{i}_LON'] = conexion[f'NUM_LONGITUDE_ESTRUTURA_{ref}']
            
            # Caso os campos de (lat, lon) sejam faltantes, pesquisa na tabela de estruturas
            is_nan = any(isnan(item) for subcoord in [[data[f'EST{i}_LAT']], [data[f'EST{i}_LON']]] for item in subcoord)
            if is_nan:
                key_ref, value_ref = 'COD_ESTRUTURA_SAP', data[f'EST{i}_SAP']
                result = [d for d in values_towers if d.get(key_ref) == value_ref]
                if len(result) != 0:
                    data[f'EST{i}_LAT'] = result[0]['NUM_LATITUDE']
                    data[f'EST{i}_LON'] = result[0]['NUM_LONGITUDE']
                else:
                    df_integrity = False
            
            if not isnan(data[f'EST{i}_LAT']) and not isnan(data[f'EST{i}_LON']):
                utm_x, utm_y = geo_conversor.get_coords_utm(data[f'EST{i}_LAT'], data[f'EST{i}_LON'])
                coords.append([utm_x, utm_y])
                data[f'EST{i}_UTM_X'] = utm_x
                data[f'EST{i}_UTM_Y'] = utm_y

            # Extraíndo informações extras sobre a torre de outro dataframe
            tower_info = [element for element in coords_towers if element['structure'] == conexion[f'COD_ESTRUTURA_{ref}_SAP']]
            if len(tower_info) != 0:
                data[f'EST{i}_ID'] = tower_info[0]['num_id']
                data[f'EST{i}_ALTURA'] = tower_info[0]['val_alt']
                data[f'EST{i}_TIPO'] = tower_info[0]['est_type']
                data[f'EST{i}_CARACT1'] = tower_info[0]['character1']
                data[f'EST{i}_CARACT2'] = tower_info[0]['character2']
        
        data['NOME_LT'] = label
        data['SAP_LT'] =  conexion['COD_LT_SAP']
        
        if len(coords) == 2:
            distance_latlon, is_same_zone = geo_conversor.geodesic_distance_latlon([data['EST1_LAT'], data['EST1_LON']], [data['EST2_LAT'], data['EST2_LON']])
            if is_same_zone == True:
                distance = geo_conversor.utm_distance_same_zone(coords[0], coords[1])
                data['DIS_M'] = distance
            else:
                data['DIS_M'] = distance_latlon

        data['VAO_CENTRO_LAT'] = conexion['NUM_LATITUDE_PONTO_CENTRAL']
        data['VAO_CENTRO_LONG'] = conexion['NUM_LONGITUDE_PONTO_CENTRAL']
        data['VAO_CENTRO_ALT_ORT'] = conexion['NUM_ALTITUDE_ORT_PONTO_CENTRAL']
    
        all_data.append(data)
    
    df = pd.DataFrame(all_data)

    # Estrutura a ordem do .csv de acordo com a numeração do conjunto de estrutruas
    df = reorganize_csv(df)

    return df, df_integrity

def convert_df_to_csv(df):
    '''
    Salva um dataframe em um arquivo .csv.

    Args:
        df (dataframe): dataframe a ser salvo.
    
    Returns:
        None
    '''
    
    return df.to_csv().encode("utf-8")

def convert_df_to_xlsx(df, label):
    '''
    Salva um dataframe em um arquivo .xlsx.

    Args:
        df (dataframe): Dataframe a ser salvo.
        label (str): Nome do arquivo a ser salvo.
    
    Returns:
        None
    '''
    
    return df.to_excel(f'out_data/{label}.xlsx', index = False)

def utm_plot(df, label):
    '''
    Visualizalizando as coordenadas UTM em um gráfico do matplotlib.

    Args:
        df (dataframe): Dataframe de referência com as conexões.
        label (str): rótulo do gráfico.
    
    Returns:
        fig (matplotlib object): Objeto com os detalhes de plotagem gráfica.
    '''

    fig, ax = plt.subplots(figsize=(10, 10))

    for index, row in df.iterrows():
        x1, y1 = row['EST1_UTM_X'], row['EST1_UTM_Y'] 
        x2, y2 = row['EST2_UTM_X'], row['EST2_UTM_Y']

        if all([x1, y1, x2, y2]):
            ax.plot([x1, x2], [y1, y2], color = 'red', lw = 2)

        if all([x1, y1]):
            ax.scatter(x1, y1, color = 'black', zorder = 5)
        
        if all([x2, y2]):
            ax.scatter(x2, y2, color = 'black', zorder = 5)

    ax.set_xlabel('Coordenada UTM (X)')
    ax.set_ylabel('Coordenada UTM (Y)')
    ax.set_title(f'{label}')

    return fig

def utm_data_dxf(df, label, scale_factor = 1000):
    '''
    Exporta a visualização das coordenadas UTM para um projeto .dxf.

    Args:
        df (dataframe): Dataframe de referência com as conexões.
        label (str): rótulo do arquivo a ser salvo.
        scale_factor (int): Fator de multiplicação da escala de renderização.
    
    Returns:
        None
    '''

    doc = ezdxf.new()
    msp = doc.modelspace()

    for index, row in df.iterrows():
        x1, y1 = row['EST1_UTM_X'] * scale_factor, row['EST1_UTM_Y'] * scale_factor
        x2, y2 = row['EST2_UTM_X'] * scale_factor, row['EST2_UTM_Y'] * scale_factor
        
        if all([x1, y1, x2, y2]):
            msp.add_line((x1, y1), (x2, y2), dxfattribs={'layer': 'Lines', 'color': 1})

        if all([x1, y1]):
            msp.add_circle((x1, y1), radius = 200, dxfattribs = {'color': 0})
            msp.add_text(row['EST1_SAP'], dxfattribs = {'insert': (x1, y1), 'height': 3000, 'color': 7})
        
        if all([x2, y2]):
            msp.add_circle((x2, y2), radius = 200, dxfattribs={'color': 0})
            msp.add_text(row['EST2_SAP'], dxfattribs = {'insert': (x2, y2), 'height': 3000, 'color': 7})

    doc.saveas(f'out_data/utm-{label}.dxf')

def plot_profile_long(profile_df, label):
    '''
    Configura os dados do gráfico para visualização no streamlit.

    Args:
        profile_df (dataframe): Dataframe com os dados para visualização do perfil longitudinal.
        label (str): Rótulo do gráfico a partir do conjunto de linhas.
    '''

    fig = go.Figure()

    fig.add_trace(go.Scatter(x = profile_df['DIS_CUM_KM'], y = profile_df['ALT_ORT'], mode = 'lines+markers',  
                  line = dict(color='blue'), marker = dict(symbol = 'circle', size = 8)))

    for i, row in profile_df.iterrows():
        fig.add_annotation(x = row['DIS_CUM_KM'], y = row['ALT_ORT'], text = row['EST_SAP'],
                           showarrow = True, arrowhead = 1, ax = 0, ay = -20, font = dict(size = 12))

    fig.update_layout(title = f'{label}', xaxis_title = 'Distância Cumulativa (km)',
                      yaxis_title = 'Altitude Ortométrica', template = 'plotly_white',  
                      xaxis = dict(tickangle = 45, rangeslider = dict(visible = True), showgrid = True, range = [0, 1]),
                      yaxis = dict(showgrid = True), height = 800)

    return fig

def main():

    # Cria uma pasta com os dados de saída caso não exista
    folder_name = 'out_data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    st.title('Trixel - Dados GEO BDIT')

    # Extraí os nomes dos conjuntos de linhas disponíveis
    lines_values = data_modules.extract_csv_attributes(csv_path = df_paths['df_path_lines'],
                                                  column_name = columns_names['column_name_lines'])
    
    # Captura o rótulo de referência do conjunto de linhas
    for i, name in enumerate(lines_values): lines_values[i] = f'{i+1}: {name}'
    label = st.selectbox(label = 'Escolha o conjunto de linhas:', options = lines_values)
    label = label.split(': ')[1]
    label = label.replace('/', '')
    
    # Realiza a extração dos dados e renderização no mapa
    try:
        m, values_towers, values_conexions, coords, zone_utm_problem = folium_map_data(label)
    except:
        info_text = '''
                    Há alguns problemas ao plotar essa linha de transmissão, 
                    futuramente iremos corrigir!
                    '''
        st.error(info_text, icon = '🚨')

        return 0

    # Botão para fazer o download das informações estruturadas em um arquivo .csv ou .xlsx
    col1, col2, col3 = st.columns([0.5, 0.25, 0.25])
    dataframe, df_integrity = make_dataset(label, values_towers, values_conexions, coords)
    with col1:
        st.warning('Baixe a tabela de conexões:')
    with col2:
        csv = convert_df_to_csv(dataframe)
        is_download = st.download_button(label = 'Baixar arquivo CSV', data = csv, file_name = f'{label}.csv')
    with col3:
        xlsx = convert_df_to_xlsx(dataframe, label)
        excel_file = f'out_data/{label}.xlsx'
        with open(excel_file, 'rb') as file:
            st.download_button(label = 'Baixar arquivo XLSX', data = file, file_name = f'{label}.xlsx')
    
    # Informa se o dataset tem dados faltantes
    if df_integrity is not True:
        info_text = '''
                    Este conjunto de dados possui informações importantes faltantes. 
                    Todos os recursos podem ser visualizados,
                    mas talvez ocorra alguma inconsistência no trecho das linhas.
                    '''
        st.error(info_text, icon = '🚨')

    map_view = st.expander(label = 'Visualização no mapa', expanded = True)

    with map_view:
        col1, col2 = st.columns(2)
        with col1:
            st.warning('Baixe o projeto para Google Earth:')
        with col2:
            # opção para exportar os dados em .kml
            kml_file = f'out_data/{label}.kml'
            with open(kml_file, "rb") as file:
                st.download_button(label = 'Baixar dados KML', data = file, file_name = f'{label}.kml')
        # Componente para visualização do mapa no streamlit
        st.components.v1.html(m._repr_html_(), height = 400, scrolling = False)

    utm_plot_view = st.expander(label = 'Visualização das coordenadas UTM', expanded = False)

    with utm_plot_view:
        col1, col2 = st.columns(2)
        with col1:
            st.warning('Baixe a visualização em CAD:')
        with col2:
            # opção para exportar os dados em .dxf
            utm_data_dxf(df = dataframe, label = label)
            dxf_file = f'out_data/utm-{label}.dxf'
            with open(dxf_file, "rb") as file:
                st.download_button(label = 'Baixar dados DXF', data = file, file_name = f'utm-{label}.dxf')
        
        if zone_utm_problem:
            error_text = '''
                         Nesse conjunto de estruturas, existe mudança de zonas UTM entre algumas coordenadas.
                         Observe que o gráfico pode apresentar inconsistências. Não se preocupe em outras inconsistências,
                         tratamos esse problema nas tabelas com os dados, no projeto .kml e no gráfico de perfil longitudinal.
                         '''
            st.error(error_text, icon = '🚨')
        # Exibindo o gráfico de coordenadas UTM
        fig = utm_plot(df = dataframe, label = label)
        st.pyplot(fig)

    
    if df_integrity:
        profile_plot_view = st.expander(label = 'Visualização do Perfil Longitudinal', expanded = False)

        with profile_plot_view: 
            
            if st.button('Gerar Perfil Longitudinal'):
                st.warning('Aguarde... Alguns dados de altitude estão sendo requeridos em uma API.')

                col1, col2, col3 = st.columns([0.5, 0.25, 0.25])
                # Visualizando um gráfico interativo do perfil longitudinal
                profile_df = data_modules.longitudinal_profile_csv(dataframe)
                with col1:
                    st.warning('Baixe os dados do perfil longitudinal:')
                with col2:
                    csv_profile = convert_df_to_csv(profile_df)
                    is_download = st.download_button(label = 'Baixar arquivo CSV', data = csv_profile, file_name = f'profile-{label}.csv')
                with col3:
                    st.button('.dxf [Em Breve]')
                fig = plot_profile_long(profile_df = profile_df, label = label)
                st.plotly_chart(fig, use_container_width = True)
    else:
        info_text = '''
                    Por problema com dados faltantes. Não conseguimos plotar a visualização do perfil longitudinal.
                    Em breve resolveremos isto!
                    '''
        st.error(info_text, icon = '🚨')

if __name__ == "__main__":
    main()

    st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #333;
        }
    </style>
    <div class="footer">
        v1.0
    </div>
    """,
    unsafe_allow_html=True
)