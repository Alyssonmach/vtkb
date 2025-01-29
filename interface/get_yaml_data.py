import yaml

# Função para carregar strings de um arquivo YAML
def load_yaml(file_path):
    '''
    Função para obtenção de dados salvos em um arquivo .yaml.

    Args:
        file_path (str): Caminho para o arquivo .yaml com os dados salvos.
    
    Return:
        data (dict): Dicionário com os dados obtidos do arquivo .yaml.
    '''

    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)  

    return data