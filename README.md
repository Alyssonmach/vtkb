# Vibra Torre [Knowledge Base] - Dados GEO BDIT
***

O principal objetivo desse repositório é tratar os dados disponibilizados pela CEMIG sobre torres, linhas de transmissão, vãos entre as estruturas e subestações. Todos os dados foram coletados da aplicação GEO BDIT, na qual é um dashboard de análise de informações e extração básica de algumas informações técnicas da CEMIG. Como o dashboard permite fazer extração de dados em pequenos lotes, os dados extraídos em [data/unprocessed-tables/](data/unprocessed-tables/) foram coletados através de uma extração manual (último acesso: `10/01/25`), na qual foi realizado diversas consultas para extrair os dados utilizando um atributo chave relacional entre as tabelas, sendo o código SAP dos conjuntos de linha (ao todo, são registrados 74 conjuntos).

## Dados tratados

A partir de uma série de tratamentos feitos nos dados para organizá-los de uma melhor forma, os mesmos podem ser encontrados em 5 tabelas distintas:

* [estruturas.csv](data/cleaned-tables/estruturas.csv): `12064` dados de torres estruturais.
* [linhas.csv](data/cleaned-tables/linhas.csv): `74` informações de conjuntos de linhas.
* [subestacoes.csv](data/cleaned-tables/subestacoes.csv): `41` subestações cadastradas.
* [vao_linhas.csv](data/cleaned-tables/vao_linhas.csv): `11990` registros de vãos entre estruturas.
* [cabos_lts.csv](data/cleaned-tables/cabos_lts.csv): `33801` Registros de cabos entre estruturas.

> OBS: Os seguintes campos de códigos SAP de estruturas são referenciados em vãos, mas não estão com registro na tabela própria das estruturas: `ESTR12701-9`, `ESTR12702-7`, `ESTR12703-5`, `ESTR12704-3`

## Análise Hierárquica das Tabelas Relacionais

Para ajudar no entedimento do uso desses dados, será descrito nas seções abaixo a estrutura e os relacionamentos entre as tabelas relacionadas à infraestrutura de transmissão de energia, incluindo cabos, estruturas, linhas de transmissão, subestações e vãos.

### 1. Tabela: [cabos_lts.csv](data/cleaned-tables/cabos_lts.csv)

Esta tabela armazena informações sobre os cabos que conectam as estruturas de transmissão, incluindo coordenadas geográficas, altitudes e distâncias.

- **Colunas**:
    - `COD_ID_CABO`: Identificador único do cabo.
    - `COD_ID_PART_CABO`: Código da parte do cabo.
    - `COD_ESTRUTURA_INI_SAP`: Código da estrutura inicial do cabo.
    - `NUM_LATITUDE_ESTRUTURA_INI`: Latitude da estrutura inicial.
    - `NUM_LONGITUDE_ESTRUTURA_INI`: Longitude da estrutura inicial.
    - `NUM_ALTITUDE_ORT_ESTRUTURA_INI`: Altitude ortométrica da estrutura inicial.
    - `NUM_ALTITUDE_GEO_ESTRUTURA_INI`: Altitude geoidal da estrutura inicial.
    - `COD_ESTRUTURA_FIM_SAP`: Código da estrutura final do cabo.
    - `COD_LT_SAP`: Código da linha de transmissão associada.
    - `VAL_DISTANCIA_PTO_MEDIO`: Distância do ponto médio do vão.
***
-  **Chaves**:
    - **Chave Primária**: `COD_ID_CABO`
    - **Chave Estrangeira**:  
        - `COD_ESTRUTURA_INI_SAP` -> Relacionada à tabela `estruturas.COD_ESTRUTURA_SAP`.
        - `COD_ESTRUTURA_FIM_SAP` -> Relacionada à tabela `estruturas.COD_ESTRUTURA_SAP`.
        - `COD_LT_SAP` -> Relacionada à tabela `linhas.CODIGO_SAP_LT`.
***
- **Relacionamentos**:
    - A tabela `cabos_lts` se relaciona com a tabela `estruturas` através das colunas `COD_ESTRUTURA_INI_SAP` e `COD_ESTRUTURA_FIM_SAP`, representando o início e o fim dos cabos.
    - A tabela também está relacionada com a tabela `linhas` pela coluna `COD_LT_SAP`, associando cada cabo a uma linha de transmissão específica.

### 2. Tabela: [estruturas.csv](data/cleaned-tables/estruturas.csv)

A tabela das estruturas contém informações sobre as estruturas que compõem as linhas de transmissão, como altura, localização e características de montagem.

- **Colunas**:
    - `VAL_ALTURA`: Altura da estrutura.
    - `COD_ESTRUTURA_SAP`: Código único da estrutura.
    - `COD_LT_SAP`: Código da linha de transmissão associada.
    - `NUM_LATITUDE`: Latitude da estrutura.
    - `NUM_LONGITUDE`: Longitude da estrutura.
    - `NUM_ALTITUDE_ORT`: Altitude ortométrica.
    - `DES_TIP_ESTRUTURA`: Tipo de estrutura (ex: autoportante, ancoragem).
***
- **Chaves**:
    - **Chave Primária**: `COD_ESTRUTURA_SAP`
    - **Chave Estrangeira**:  
        - `COD_LT_SAP` -> Relacionada à tabela `linhas.CODIGO_SAP_LT`.
***
- **Relacionamentos**:
    - A tabela `estruturas` está conectada à tabela `linhas` através da coluna `COD_LT_SAP`, indicando que cada estrutura pertence a uma linha de transmissão específica.

### 3. Tabela: [linhas.csv](data/cleaned-tables/linhas.csv)

A tabela dos conjuntos de linha descreve as linhas de transmissão, incluindo a tensão de operação e o status da linha.

- **Colunas**:
    - `NOME_DA_LT_-_SAP`: Nome da linha de transmissão.
    - `CODIGO_SAP_LT`: Código único da linha de transmissão.
    - `ID_LT`: Identificador da linha de transmissão.
    - `TENSAO_DE_OPERACAO`: Tensão de operação da linha de transmissão.
    - `STATUS_DA_LT`: Status da linha de transmissão.
***
- **Chaves**:
    - **Chave Primária**: `CODIGO_SAP_LT`
***
- **Relacionamentos**:
    - A tabela `linhas` se relaciona com as tabelas `cabos_lts` e `estruturas` por meio das colunas `CODIGO_SAP_LT` e `COD_LT_SAP`, respectivamente.

### 4. Tabela: [subestacoes.csv](data/cleaned-tables/subestacoes.csv)

Esta tabela contém informações sobre as subestações, incluindo suas localizações e identificações.

- **Colunas**:
    - `COD_SE_SAP`: Código único da subestação.
    - `NOM_SE_SAP`: Nome da subestação.
    - `NUM_LATITUDE`: Latitude da subestação.
    - `NUM_LONGITUDE`: Longitude da subestação.
***
- **Chaves**:
    - **Chave Primária**: `COD_SE_SAP`
***
- **Relacionamentos**:
    - Não há relações diretas com outras tabelas especificadas, mas as subestações podem estar associadas à infraestrutura de linhas de transmissão de maneira indireta.

### 5. Tabela: [vao_linhas.csv](data/cleaned-tables/vao_linhas.csv)

Essa tabela descreve os vãos entre as estruturas das linhas de transmissão, incluindo informações sobre as distâncias e altitudes.

- **Colunas**:
    - `COD_VAO_SAP`: Código único do vão.
    - `COD_ESTRUTURA_INI_SAP`: Código da estrutura inicial.
    - `COD_ESTRUTURA_FIM_SAP`: Código da estrutura final.
    - `VAL_LARGURA_FAIXA_ESQ`: Largura da faixa do lado esquerdo do vão.
    - `VAL_LARGURA_FAIXA_DIR`: Largura da faixa do lado direito do vão.
***
- **Chaves**:
    - **Chave Primária**: `COD_VAO_SAP`
    - **Chave Estrangeira**:  
        - `COD_ESTRUTURA_INI_SAP` -> Relacionada à tabela `estruturas.COD_ESTRUTURA_SAP`.
        - `COD_ESTRUTURA_FIM_SAP` -> Relacionada à tabela `estruturas.COD_ESTRUTURA_SAP`.
        - `COD_LT_SAP` -> Relacionada à tabela `linhas.CODIGO_SAP_LT`.
***
- **Relacionamentos**:
    - A tabela `vao_linhas` se conecta às tabelas `estruturas` e `linhas`, através das colunas `COD_ESTRUTURA_INI_SAP`, `COD_ESTRUTURA_FIM_SAP`, e `COD_LT_SAP`, representando os vãos entre as estruturas e sua associação com as linhas de transmissão.

## Scripts automatizados de tratamendo dos dados (Python 3.12.8)

* [Concatenação dos arquivos .csv das estruturas](cli-commands/concatenate_csv.py):

Esse script CLI tem como objetivo concatenar diversas tabelas de estruturas extraídas no APP GEO BDIT no formato .csv em uma única tabela. Para executá-lo, segue um template abaixo:

```bash
python .\concatenate_csv.py --src_path <pasta-de-origem/> --dst_path <pasta-de-destino/> --filename <nome-do-arquivo.csv> 
```

* [Tratamento dos arquivos .csv extraídos](cli-commands/csv_edit.py):

Esse script CLI tem como objetivo normalizar alguns padrões no dataframe, sendo eles:
    * Eliminar duplicatas de linhas;
    * Normalizar a tipagem do nome das colunas de atributos (remoção de espaçamento e acentos);
    * Eliminar colunas completas que constam como vazias ou desnecessárias;

Para executá-lo, segue um template abaixo:

```bash
python .\csv_edit.py --src_path <arquivo-origem.csv> --dst_path  <pasta-de-destino/> --filename <nome-do-arquivo.csv> --drop_duplicates <True or False> --sanitize_column_names <True or False> --drop_columns <col1 col2 col3...>
```

* [Renomeação em lotes de arquivos .csv](cli-commands/rename_files_by_values.py):

Renomeia um lote de arquivos .csv com base em um atributo chave de uma coluna (o valor desse atributo deve ser constante para todos os elemtnos da tabela). Para executá-lo, segue um template abaixo:

```bash
python .\rename_files_by_values.py --folder_path <pasta-origem> --column_name <nome-coluna>
```

### Ajuda com os parâmetros dos scripts CLI

Para mais informações sobre os parâmetros dos scripts CLI, tente executar o comando abaixo, ele mostrará em mais detalhes como deve ser organizado os parâmetros de entrada e saída do script.

```bash
python .<nome-script>.py --help
```



