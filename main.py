try:
    import os

    '''
    os.system('python -m pip install --upgrade pip')
    os.system('pip install -r requirements.txt')
    os.system('cls')
    '''

    try:
        from sped_vs_sefaz import sped_vs_sefaz

        sped_vs_sefaz()
    except Exception as e:
        print(f'Ocorreu um erro inesperado ao executar o programa: {e}')
        os.system('pause')
        
except Exception as e:
    print(f'Ocorreu um erro ao instalar as dependências: {e}')
    os.system('pause')