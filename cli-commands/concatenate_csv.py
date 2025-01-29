from bdit_data import data_analysis
import argparse

def help_texts():
    '''
    Textos de ajuda do argparser.

    Chaves de acesso: `text_description`, `dst_path_help`, `src_path_help` e `filename_help`.
    
    Args:
        None

    Returns:
        texts (dict): Dicionário com as informações de ajuda de cada parâmetro do argparser.
    '''

    texts = {
        'text_description': '(str) Concatena arquivos csv em um único arquivo.',
        'src_path_help': '(str) Caminho onde está localizado os arquivos .csv das torres.',
        'dst_path_help': '(str) Caminho de destino a ser salvo o dataframe concatenado .csv.',
        'filename_help': '(str) Nome do arquivo .csv com os dataframes concatenados, extensão deve ser declarada.'
    }

    return texts

def main():

    # Obtém os campos de texto com informações de ajuda
    texts = help_texts()
    # Adiciona uma descrição do comando
    parser = argparse.ArgumentParser(texts['text_description'])

    # Define os parâmetros de entrada
    parser.add_argument('--src_path', type = str, help = texts['src_path_help'], required = True)
    parser.add_argument('--dst_path', type = str, help = texts['dst_path_help'], default = '')
    parser.add_argument('--filename', type = str, help = texts['filename_help'], default = 'output.csv')

    # Atribuí a args os dados coletados da linhas de comando
    args = parser.parse_args()

    # Concatena um diretório de arquivos .csv em um arquivo único
    try:
        data = data_analysis()
        dataframe = data.concatenate_csv(args.src_path)
        full_path = args.dst_path + args.filename
        data.df_to_csv(dataframe, dst_path = full_path)

        print(f'Tabela gerada com sucesso em {full_path}.')
    except Exception as e:
        print('Erro ao executar concatenação, revise os dados de entrada.')
        print(f'Erro gerado\n: {e}')

if __name__ == '__main__':
    main()