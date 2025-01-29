from get_yaml_data import load_yaml

def return_data_paths(yaml_file):
    '''
    Retorna os caminhos das tabelas com os dados do GEO BDIT tratados.

    Args:
        yaml_file (str): Caminho do arquivo .yaml com a localização dos dataframes.
    
    Returns:
        df_paths (dict): Dicionário com os caminhos de referência: `df_path_lines` para o
        dataframe das linhas, `df_path_towers` para o dataframe das estruturas e `df_path_conexions`
        para o dataframe das conexões.
    '''
    
    data = load_yaml(file_path = yaml_file)

    df_paths = {'df_path_lines': data['df_path_lines'],
                'df_path_towers': data['df_path_towers'],
                'df_path_conexions': data['df_path_conexions']}

    return df_paths

def return_columns_ref(yaml_file):
    '''
    Retorna o nome das colunas de referência para acesso do conjunto das linhas.

    Args:
        yaml_file (str): Caminho do arquivo .yaml com a localização dos dataframes.
    
    Returns:
        columns_ref (dict): Dicionário com o nome das colunas de referência. `column_name_lines`
        para o nome do atributo que tem as informações dos conjuntos de linhas, `column_sap_lines` 
        para o código sap dos conjuntos de linhas e `column_name_towers` para o nome dos conjuntos
        de linhas na tabela de estruturas.
    '''

    data = load_yaml(file_path = yaml_file)

    columns_ref = {'column_name_lines': data['column_name_lines'],
                   'column_sap_lines': data['column_sap_lines'],
                   'column_name_towers': data['column_name_towers']}

    return columns_ref