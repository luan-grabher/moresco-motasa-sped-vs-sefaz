from comparativo import getComparacaoSefazSped
from relatorio import createRelatorio
from sefaz import getArquivoSefazFromUser, getNotasFromSefaz
from easygui import msgbox
from sped import getArquivoSpedFromUser, getNotasFromSped
import traceback

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

        comparacao = getComparacaoSefazSped(notas_sefaz, notas_sped)

        createRelatorio(comparacao)

    except Exception as e:
        msgbox('Ocorreu um erro inesperado, verifique o log para mais detalhes')
        print(traceback.format_exc())
        input('Pressione qualquer tecla para sair')
        exit()

if __name__ == '__main__':
    sped_vs_sefaz()
