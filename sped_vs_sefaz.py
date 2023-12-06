


from sefaz import getArquivoSefazFromUser, getNotasFromSefaz
from easygui import msgbox

from sped import getArquivoSpedFromUser, getNotasFromSped

def sped_vs_sefaz():
    try:
        arquivo_sefaz = getArquivoSefazFromUser()
        if not arquivo_sefaz:
            msgbox('Nenhum arquivo SEFAZ selecionado')
            exit()

        arquivo_sped = getArquivoSpedFromUser()
        if not arquivo_sped:
            msgbox('Nenhum arquivo SPED selecionado')
            exit()

        notas_sefaz = getNotasFromSefaz(arquivo_sefaz)
        notas_sped = getNotasFromSped(arquivo_sped)

    except Exception as e:
        #TODO: Exibir erro para o usuário
        print(e)
        exit()

if __name__ == '__main__':
    sped_vs_sefaz()
