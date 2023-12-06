
from easygui import fileopenbox, msgbox
import pandas

def getArquivoSefazFromUser():
    msgbox('Selecione o arquivo txt do relatório do SEFAZ de entradas ou Saidas')

    return fileopenbox(msg='Selecione o arquivo txt do relatório do SEFAZ de entradas ou Saidas',
                       title='Relatório txt do SEFAZ',
                       default='*.txt',
                       filetypes='*.txt',
                       multiple=False)

colunas_arquivo_sefaz = ['dt_Emit', 'CNPJ_Emit', 'Razao_Social_Emit', 'Numero', 'Total_NF-e', 'Total_ICMS', 'Chave_NF-e']

def getNotasFromSefaz(arquivo_sefaz):
    return pandas.read_csv(arquivo_sefaz, sep=';', encoding='latin-1', usecols=colunas_arquivo_sefaz)

def getNotaSefaz(notas_sefaz, chave_nfe):
    return notas_sefaz.loc[notas_sefaz['Chave_NF-e'] == chave_nfe]

if __name__ == '__main__':
    arquivo_teste = './downloads/sefaz.txt'
    notas = getNotasFromSefaz(arquivo_teste)

    print(notas)