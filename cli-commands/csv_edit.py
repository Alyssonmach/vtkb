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
        'text_description': '(str) Trata os dados do dataframe CSV.',
        'src_path_help': '(str) Caminho onde está localizado o arquivo .csv de referência.',
        'dst_path_help': '(str) Caminho onde o dataframe .csv tratado será salva.',
        'filename_help': '(str) Nome do arquivo .csv onde o dataframe tratado será salvo.',
        'drop_duplicates_help': '(bool) Elimina linhas duplicadas do dataframe.',
        'sanitize_column_names_help': '(str) Normaliza adequadamente o nome dos atributos do dataframe.',
        'drop_columns_help': '(list) Elimina colunas delimitadas do dataframe.'
    }

    return texts

def main():

    # Obtém os campos de texto com informações de ajuda
    texts = help_texts()
    # Adiciona uma descrição do comando
    parser = argparse.ArgumentParser(texts['text_description'])

    # Define os parâmetros de entrada
    parser.add_argument('--src_path', type = str, help = texts['src_path_help'], required = True)
    parser.add_argument('--dst_path', type = str, help = texts['dst_path_help'], default = '.')
    parser.add_argument('--filename', type = str, help = texts['filename_help'], default = 'output.csv')
    parser.add_argument('--drop_duplicates', type = bool, help = texts['drop_duplicates_help'], default = False)
    parser.add_argument('--sanitize_column_names', type = bool, help = texts['sanitize_column_names_help'], default = False)
    parser.add_argument('--drop_columns', type = str, help = texts['drop_columns_help'], nargs = '+')

    # Atribuí a args os dados coletados da linhas de comando
    args = parser.parse_args()

    try:
        data = data_analysis()
        dataframe = data.csv_to_df(args.src_path)

        # Elimina linhas duplicadas da tabela
        if args.drop_duplicates:
            print('Eliminando duplicatas...')
            original_dim = data.verify_dimension(dataframe)
            dataframe, copies = data.separate_repeated_data(dataframe)
            new_dim = data.verify_dimension(dataframe)
        
            if original_dim == new_dim: 
                print('Nenhuma duplicada encontrada.')
            else:
                print('Duplicatas removidas com sucesso!')
                print(f'Dimensão dos dados antes: {original_dim}\nDimensão dos dados depois: {new_dim}')
                print(f'Dados repetidos: {copies.reset_index(drop = True)}\n\n\n')
        
        # Elimina colunas especificadas
        if args.drop_columns is not None:
            print(f'Eliminando as colunas {args.drop_columns}...')
            original_dim = data.verify_dimension(dataframe)
            dataframe = data.drop_columns(dataframe, columns_list = args.drop_columns)
            new_dim = data.verify_dimension(dataframe)

            if original_dim == new_dim: 
                print('Nenhuma duplicada encontrada.')
            else:
                print('Colunas removidas com sucesso!')
                print(f'Dimensão dos dados antes: {original_dim}\nDimensão dos dados depois: {new_dim}\n\n\n')
        
        # Normaliza o nome dos atributos do datafram
        if args.sanitize_column_names:
            dataframe = data.sanitize_column_names(dataframe = dataframe)
            print('Normalização do nome dos atributos feitas com sucesso!\n\n\n')

        print('Operações concluídas, salvando o dataframe em um arquivo .csv...')
        full_path = args.dst_path + args.filename
        data.df_to_csv(dataframe, dst_path = full_path)
        print(f'Tabela gerada com sucesso em {full_path}.')

    except Exception as e:
        print('Erro ao executar procedimentos, revise os dados de entrada.')
        print(f'Erro gerado\n: {e}')

if __name__ == '__main__':
    main()