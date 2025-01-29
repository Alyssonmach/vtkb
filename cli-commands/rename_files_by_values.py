from bdit_data import data_analysis
import pandas as pd
import argparse
import os

def help_texts():
    '''
    Textos de ajuda do argparser.

    Chaves de acesso: `folder_path`, e `column_name`.
    
    Args:
        None

    Returns:
        texts (dict): Dicionário com as informações de ajuda de cada parâmetro do argparser.
    '''

    texts = {
        'text_description': '(str) Renomeia vários arquivos .csv a partir de um atributo de referência.',
        'folder_path_help': '(str) Caminho onde os arquivos .csv se encontram.',
        'column_name_help': '(str) Nome da coluna que contém os valores a serem especificados.'
    }

    return texts

def main():
    
     # Obtém os campos de texto com informações de ajuda
    texts = help_texts()
    # Adiciona uma descrição do comando
    parser = argparse.ArgumentParser(texts['text_description'])

    # Define os parâmetros de entrada
    parser.add_argument('--folder_path', type = str, help = texts['folder_path_help'], required = True)
    parser.add_argument('--column_name', type = str, help = texts['column_name_help'], required = True)

    # Atribuí a args os dados coletados da linhas de comando
    args = parser.parse_args()

    # Renomeia um diretório de arquivos .csv a partir de um atributo chave
    data = data_analysis()
    data.rename_csv_files(folder_path = args.folder_path, column_name = args.column_name)

if __name__ == '__main__':
    main()
