import os

def start_streamlit_server(script_file = 'main.py'):
    '''
    Inicia um server local para renderizar a interface com o streamlit.

    Args:
        script_file (str): Caminho do arquivo python para renderizar a interface streamlit.
    
    Returns:
        None
    '''

    os.system(f'streamlit run {script_file}')

if __name__ == "__main__":
    start_streamlit_server()
