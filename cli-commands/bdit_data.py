import pandas as pd
import unicodedata
import os

class data_analysis:
    '''
    Funções utilitárias para realizar uma série de tratamentos nos dataframes.
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

    def concatenate_csv(self, src_path):
        '''
        Concatena arquivos csv com atributos iguais em um arquivo único.

        Args:
            src_path (str): Caminho de destino onde estão localizados os arquivos .csv.
        
        Returns:
            full_df (dataframe): Dataframe no formato do pandas com as tabelas concatenadas.
        '''

        # Lê todos os arquivos .csv existentes no diretório
        archives_csv = [f for f in os.listdir(src_path) if f.endswith('.csv')]
        dataframes = list()

        # Converte os arquivos .csv para dataframes e adiciona a uma lista
        for archive in archives_csv:
            full_path = os.path.join(src_path, archive)
            df = pd.read_csv(full_path, quoting = 3)
            dataframes.append(df)
        
        # Concatena os dataframes em um arquivo único
        full_df = pd.concat(dataframes, ignore_index = True)

        return full_df
    
    def csv_to_df(self, src_path):
        '''
        Converte um arquivo .csv para um dataframe do Pandas.

        Args:
            src_path (str): Caminho onde está localizado o arquivo .csv.
        
        Returns:
            dataframe (dataframe): Dados no formato de dataframe do Pandas.
        '''

        return pd.read_csv(src_path, sep = ';', encoding='utf-8-sig', header = 0, na_values=[''])


    def df_to_csv(self, dataframe, dst_path):
        '''
        Salva um dataframe do pandas em um arquivo .csv.

        Args:
            dataframe (dataframe): Dataframe a ser salvo em um arquivo .csv.
            dst_path (str): Caminho com o nome do arquivo .csv a ser salvo.
        
        Returns:
            None
        '''

        dataframe.to_csv(dst_path, index = False)
    
    def separate_repeated_data(self, dataframe, save_as_csv = False, dst_path = ''):
        '''
        Descarta linhas duplicadas em um dataframe do Pandas.

        Args:
            dataframe (dataframe): Dataframe original a ser verificada as duplicatas.
        
        Returns:
            unique (dataframe): Dataframe sem as duplicatas mantidas.
            copies (dataframe): Tabela com as duplicadas removidas.
        '''

        # Extraí para outro dataframe as linhas com repetição
        duplicates = dataframe[dataframe.duplicated(keep = False)] 
        unique = dataframe.drop_duplicates(keep = 'first')
        copies = duplicates[duplicates.duplicated(keep = 'first')]

        # Sobrescreve o arquivo .csv com as repetições removidas
        if save_as_csv:
            self.df_to_csv(unique, dst_path = dst_path)

        return unique, copies
    
    def verify_dimension(self,dataframe):
        '''
        Verifica a dimensão da tabela.

        Args:
            dataframe (dataframe): Dataframe Pandas de referência.
        
        Returns:
            shape (list): Informa a quantidade de `(linhas, colunas)`.
        '''

        return dataframe.shape
    
    def drop_columns(self, dataframe, columns_list):
        '''
        Elimina uma lista de colunas do dataframe Pandas.

        Args:
            dataframe (dataframe): Dataframe de referência.
            columns_list (list): Lista de colunas a serem deletadas.
        
        Returns:
            dataframe (dataframe): Dataframe com as colunas excluídas.
        '''

        for column in columns_list:
            dataframe.drop(columns = column, inplace = True)

        return dataframe
    
    def rename_csv_files(self, folder_path, column_name):
        '''
        Renomeia arquivos .csv em uma pasta baseado em valores específicos de uma coluna de referência.

        Args:
            folder_path (str): Caminho para a pasta que contém os arquivos .csv.
            column_name (str): Nome da coluna com o valor de referência para substituir nos arquivos.
        
        Returns:
            None
        '''

        # Intera sobre os arquivos
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(folder_path, file_name)
                
                try:
                    df = self.csv_to_df(src_path = file_path)

                    # Checha se a coluna existe no dataframe
                    if column_name in df.columns:
                        # Extraí o valor da coluna 
                        new_name = df[column_name].dropna().iloc[0]

                        # Verifica se o valor é uma string válida
                        if isinstance(new_name, str):
                            # Organiza o novo nome do arquivo
                            new_file_name = f"{new_name}.csv"
                            new_file_path = os.path.join(folder_path, new_file_name)

                            # Renomeia o arquivo
                            os.rename(file_path, new_file_path)
                            print(f'Arquivo "{file_name}" renomeado para "{new_file_name}"')
                        else:
                            print(f'Ignorando "{file_name}": Nome inválido para preenchimento')
                    else:
                        print(f'Ignorando "{file_name}": Coluna "{column_name}" não encontrada')
                except Exception as e:
                    print(f'Erro ao processar o arquivo "{file_name}": {e}')
    
    def sanitize_name(self, name):
        '''
        Corrige problemas de formatação com o nome de cada campo dos dataframes.

        Args: 
            name (str): Conteúdo de título da tabela.
        
        Returns:
            name (str): Conteúdo de título da tabela formatado.
        '''

        # Substitui espaços na string por um caracter válido
        name = name.replace(" ", "_")
        # Remove acentuação da letra
        name = ''.join((c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn'))

        return name

    def sanitize_column_names(self, dataframe):
        '''
        Corrige problemas de formatação nos nomes dos campos dos dataframes.

        Args:
            dataframe (str): Dataframe de referência com o nome dos atributos sem normalização.
        
        Returns:
            dataframe (dataframe): Dataframe do pandas com correção de tipo no nome dos atributos.
        '''

        dataframe.columns = [self.sanitize_name(col) for col in dataframe.columns]

        return dataframe

