from geo_coords import coords_analysis
from math import isnan
import pandas as pd 
import time

class render_data:
    '''
    Módulos para manipulação de dados para renderização na interface.
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
    
    def extract_csv_attributes(self, csv_path, column_name):
        '''
        Lê um arquivo .csv, extrai os valores de uma coluna especifica e retorna uma lista contendo
        os atributos de string.

        Args:
            csv_path (str): Caminho para o arquivo .csv.
            column_name (str): Nome da coluna que será extraído os dados.
        
        Returns:
            attributes_list (str): Lista de valores da coluna especificada.
        '''

        try:
            df = pd.read_csv(csv_path)

            if column_name not in df.columns:
                raise ValueError(f'A coluna {column_name} não foi encontrado no arquivo.')
            
            attributes_list = df[column_name].dropna().astype(str).tolist()

            return attributes_list
        except Exception as e:
            print(f'Erro: {e}')

            return list()
    
    def search_values_attributes(self, csv_path, column_name, search_value):
        '''
        Busca um valor específico em uma coluna e retorna um dicionário com os 
        atributos da linha correspondente.

        Args:
            csv_path (str): Caminho para o arquivo .csv.
            column_name (str): Nome da coluna que será extraído os dados.
            search_values (str): Valor a ser pesquisado na coluna.
        
        Returns:
            attributes_dict (dict): Dicionário contendo os atributos da linha encontrada.
        '''

        try:
            df = pd.read_csv(csv_path)

            if column_name not in df.columns:
                raise ValueError(f'A coluna "{column_name}" não foi encontrada no arquivo.')
            
            line = df[df[column_name] == search_value]

            if line.empty:
                raise ValueError(f"O valor '{search_value}' não foi encontrado na coluna '{column_name}'.")
                
            attributes_dict = line.iloc[0].to_dict()

            return attributes_dict
        
        except Exception as e:
            print(f"Erro: {e}")

            return list
        
    def search_multiples_values_attributes(self, csv_path, column_name, search_value):
        '''
        Busca todas as ocorrências de um valor específico em uma coluna e retorna uma 
        lista de dicionários com os atributos das linhas correspondentes.
        
        Args:
            csv_path (str): Caminho para o arquivo .csv.
            column_name (str): Nome da coluna onde será feita a pesquisa.
            search_value (str): Valor a ser pesquisado na coluna.
        
        Returns:
            attributes_lines (list): Lista de dicionários com os atributos das linhas encontradas.
        '''

        try:
            df = pd.read_csv(csv_path)
            
            if column_name not in df.columns:
                raise ValueError(f"A coluna '{column_name}' não foi encontrada no arquivo.")
            
            lines = df[df[column_name] == search_value]
            
            if lines.empty:
                raise ValueError(f"O valor '{search_value}' não foi encontrado na coluna '{column_name}'.")
            
            attributes_lines = lines.to_dict(orient = 'records')

            return attributes_lines
        except Exception as e:
            print(f"Erro: {e}")

            return list()
    
    def separate_conj_data(self, df_paths, columns_names, label):
        '''
        Retorna os dados extraídos separados por conjunto de linhas.

        Args:
            df_paths (dict): df_paths (dict): Dicionário com os caminhos de referência: `df_path_lines` para o
            dataframe das linhas, `df_path_towers` para o dataframe das estruturas e `df_path_conexions`
            para o dataframe das conexões.
            columns_names (dict): columns_ref (dict): Dicionário com o nome das colunas de referência. `column_name_lines`
            para o nome do atributo que tem as informações dos conjuntos de linhas, `column_sap_lines` 
            para o código sap dos conjuntos de linhas e `column_name_towers` para o nome dos conjuntos
            de linhas na tabela de estruturas.

        Returns:
            value_towers (dict): Dicionário com os dados das estruturas do conjunto.
            coords (dict): Informações sobre as torres de transmissão. `lat` informação sobre a latitude, `long` informação sobre a 
            longitude, `alt_ort` dados da altitude ortogonal, `num_id` numeração da torre no conjunto, `est_type` tipo de estrutura, `character1`
            característica primária da estrutura, `character2` característica secundária da estrutura e `val_alt` a informação da altura da estrutura.
            values_conexions (dict): Dicionário com os dados das conexões entre estruturas do conjunto.
        '''

        values_lines = self.search_values_attributes(csv_path = df_paths['df_path_lines'], column_name = columns_names['column_name_lines'],
                                                     search_value = label)
        values_towers = self.search_multiples_values_attributes(csv_path = df_paths['df_path_towers'], column_name = columns_names['column_name_towers'],
                                                                search_value = values_lines[columns_names['column_sap_lines']]) 
        
        # Adiciona as informações da estrutura do conjunto em uma lista
        coords = list()
        for value in values_towers:

            lat, long, structure = value['NUM_LATITUDE'], value['NUM_LONGITUDE'], value['COD_ESTRUTURA_SAP']
            alt_ort, num_id, est_type = value['NUM_ALTITUDE_ORT'], value['NUM_ID_SEQUENCIA'], value['DES_TIP_ESTRUTURA']
            character1, character2 = value['DES_CARACTERISTICA1'], value['DES_CARACTERISTICA2']
            val_alt = value['VAL_ALTURA']
            coords.append({'lat': lat, 'long': long, 'structure': structure, 'alt_ort': alt_ort, 'num_id': num_id,
                           'est_type': est_type, 'character1': character1, 'character2': character2, 'val_alt': val_alt})

        values_conexions = self.search_multiples_values_attributes(csv_path = df_paths['df_path_conexions'], column_name = columns_names['column_name_towers'],
                                                                   search_value = values_lines[columns_names['column_sap_lines']])
        
        return values_towers, coords, values_conexions

    def compose_alt_ort(self, df):
        '''
        Adiciona altitudes ortométricas no dataframe caso sejam faltantes.

        Args:
            df (dataframe): Dataframe com os dados salvos.
        
        Returns:
            df (dataframe): Dataframe com os campos de altitude ortométricas corrigidos.
        '''

        data = coords_analysis()

        def interate_alt_ort_ini(row):
            if row['EST1_ALT_ORT'] == 0.0 or isnan(row['EST1_ALT_ORT']) == True:
                if all([row['EST2_LAT'], row['EST2_LON']]) is not False:
                    if all([row['EST1_LAT'], row['EST1_LON']]):
                        time.sleep(1)
                        row['EST1_ALT_ORT'] = data.get_altitude_ort(latitude = row['EST1_LAT'], longitude = row['EST1_LON'])
            
            return row
        
        def interate_alt_ort_fin(row):
            if row['EST2_ALT_ORT'] == 0.0 or isnan(row['EST2_ALT_ORT']) == True:
                if all([row['EST2_LAT'], row['EST2_LON']]):
                    time.sleep(1)
                    row['EST2_ALT_ORT'] = data.get_altitude_ort(latitude = row['EST2_LAT'], longitude = row['EST2_LON'])
            
            return row
    
        df = df.apply(interate_alt_ort_ini, axis = 1)
        df = df.apply(interate_alt_ort_fin, axis = 1)

        return df
    
    def meters_to_km(self, meters): 
        '''
        Converte uma distância de metros para quilômetros.

        Args:
            meters (float): Distância em metros.
        
        Returns:
            km (float): Distância em quilômetros.
        '''
        km = meters / 1000

        return km
    
    def longitudinal_profile_csv(self, df):
        '''
        Organiza um dataframe com os dados para plotagem do perfil longitudinal.

        Args:
            df (dataframe): Dataframe de referência com todos os dados do conjunto de torres.

        Returns:
            profile_df (dataframe): Dataframe com os dados do perfil longitudinal. 
        '''

        # Preenche os campos de altitude ortométricas caso seja faltante
        df = self.compose_alt_ort(df)
        
        profile_df = pd.DataFrame(columns = ['EST_SAP', 'ALT_ORT', 'DIS_CUM_KM'])
        sum_distance = 0
        for index, (_, row) in enumerate(df.iterrows()):
            if index == 0:
                new_line = pd.DataFrame({'EST_SAP': [row['EST1_SAP']], 'ALT_ORT': [row['EST1_ALT_ORT']], 'DIS_CUM_KM': [self.meters_to_km(sum_distance)]})
                profile_df = pd.concat([profile_df, new_line], ignore_index = True)
                sum_distance += row['DIS_M']
                new_line = pd.DataFrame({'EST_SAP': [row['EST2_SAP']], 'ALT_ORT': [row['EST2_ALT_ORT']], 'DIS_CUM_KM': [self.meters_to_km(sum_distance)]})
                profile_df = pd.concat([profile_df, new_line], ignore_index = True)
            else:
                sum_distance += row['DIS_M']
                new_line = pd.DataFrame({'EST_SAP': [row['EST2_SAP']], 'ALT_ORT': [row['EST2_ALT_ORT']], 'DIS_CUM_KM': [self.meters_to_km(sum_distance)]})
                profile_df = pd.concat([profile_df, new_line], ignore_index = True)
        
        return profile_df
    



