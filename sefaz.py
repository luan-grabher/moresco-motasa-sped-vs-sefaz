
import os
from easygui import fileopenbox, msgbox, diropenbox
import pandas


colunas_arquivo_sefaz = ['dt_Emit', 'CNPJ_Emit', 'Razao_Social_Emit', 'Numero', 'Total_NF-e', 'Total_ICMS', 'Chave_NF-e']


def getArquivoSefazFromUser(selecionar_pasta = False):
    if not selecionar_pasta:
        msgbox('Selecione o arquivo txt do relatório do SEFAZ de entradas ou Saidas')

        return fileopenbox(msg='Selecione o arquivo txt do relatório do SEFAZ de entradas ou Saidas',
                        title='Relatório txt do SEFAZ',
                        default='*.txt',
                        filetypes='*.txt',
                        multiple=False)
    
    else:
        msgbox('Selecione a pasta com os arquivos txt do relatório do SEFAZ de entradas ou Saidas')

        path_pasta_com_Arquivos = diropenbox(msg='Selecione a pasta com os arquivos txt do relatório do SEFAZ de entradas ou Saidas.\nOs arquivos devem ser .txt e possuir "sefaz" no nome.',
                        title='Relatório txt do SEFAZ')
        
        if not path_pasta_com_Arquivos:
            return None
        
        arquivos_sefaz = []
        for arquivo in os.listdir(path_pasta_com_Arquivos):
            if arquivo.endswith(".txt") and  'sefaz' in arquivo.lower():
                arquivos_sefaz.append(path_pasta_com_Arquivos + '\\' + arquivo)
        
        return arquivos_sefaz

def getNotasFromSefaz(arquivo_sefaz):
    if type(arquivo_sefaz) == list:
        print('Concatenando arquivos SEFAZ')

        notas = pandas.DataFrame(columns=colunas_arquivo_sefaz)
        for arquivo in arquivo_sefaz:
            notas = pandas.concat([notas, getNotasFromCSV(arquivo)])
        return notas
    
    else:
        return getNotasFromCSV(arquivo_sefaz)

def getNotasFromCSV(arquivo_sefaz):
    try:
        return pandas.read_csv(arquivo_sefaz, sep=';', encoding='latin-1', usecols=colunas_arquivo_sefaz)
    except Exception as e:
        print('Erro ao ler arquivo SEFAZ: {}'.format(arquivo_sefaz))

        return pandas.DataFrame(columns=colunas_arquivo_sefaz)

def getNotaSefaz(notas_sefaz, chave_nfe):
    return notas_sefaz.loc[notas_sefaz['Chave_NF-e'] == chave_nfe]


# (Opcional) Usuario pode escolher mais de uma pasta e o robo seelciona [ ]s arquivos .txt que tenham as colunas do sefaz separadas por ; e junta [ ]s em um array só. (Caso fizer deixa em stand by comentado e pergunta para elas se é assim ou não)

if __name__ == '__main__':
    arquivo_teste = './downloads/sefaz.txt'
    notas = getNotasFromSefaz(arquivo_teste)
    print('Notas encontradas no arquivo: {}'.format(len(notas)))

    arquivos_sefaz = getArquivoSefazFromUser(selecionar_pasta=True)
    notas = getNotasFromSefaz(arquivos_sefaz)
    print('Notas encontradas na pasta: {}'.format(len(notas)))
