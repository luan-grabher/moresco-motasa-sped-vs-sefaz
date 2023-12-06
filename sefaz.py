
from easygui import fileopenbox, msgbox
import pandas

def getArquivoSefazFromUser():
    msgbox('Selecione o arquivo txt do relatório do SEFAZ de entradas ou Saidas')

    return fileopenbox(msg='Selecione o arquivo txt do relatório do SEFAZ de entradas ou Saidas',
                       title='Relatório txt do SEFAZ',
                       default='*.txt',
                       filetypes='*.txt',
                       multiple=False)

colunas_arquivo_sefaz = ['dt_Emit', 'Dt_Ent/Sai', 'IE_Emit', 'UF_Emit', 'CNPJ_Emit', 'Razao_Social_Emit', 'IE_Dest/Remet', 'UF_Dest/Remet', 'CNPJ_Dest/Remet', 'Razao_Social_Dest/Remet', 'Mod', 'Serie', 'Numero', 'Total_NF-e', 'Total_BC_ICMS', 'Total_ICMS', 'Total_BC_ICMS_ST', 'Total_ICMS_ST', 'Sit', 'E/S', 'Chave_NF-e']

def getNotasFromSefaz(arquivo_sefaz):
    return pandas.read_csv(arquivo_sefaz, sep=';', encoding='latin-1', usecols=colunas_arquivo_sefaz)
