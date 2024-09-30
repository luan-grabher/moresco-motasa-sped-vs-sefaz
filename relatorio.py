import os

from easygui import msgbox
import pandas as pd
import openpyxl
from comparativo import getComparacaoSefazSped

from sefaz import getNotasFromSefaz
from sped import getNotasFromSped


'''
    1. Analise das notas fiscais constantes no arquivo SPED que não constam no sefaz – relação de notas com o número da nota.
    2. Analise das notas fiscais constantes no sefaz que não constam no arquivo SPED – relação de notas trazendo o número da nota, data, valor e CNPJ do emitente.
    3. Analise do total da NFE Sped + campo ICMS x Total da NFE sefaz + campo ICMS – relação de notas divergentes pelo número da nota
    4. Com base no resultado do item 3, fazer a análise individual por nota do arquivo SPED buscando a nota com o CFOP/valor/ ICMS x Sefaz nota e valor ICMS – relação de notas
'''

def getTableNotasSpedQueNaoEstaoNoSefaz(notas_sped_que_nao_estao_no_sefaz) -> pd.DataFrame:
    # Notas SPED que não estão no SEFAZ
    
    df_notas_sped_que_nao_estao_no_sefaz = pd.DataFrame()
    df_notas_sped_que_nao_estao_no_sefaz['Chave da nota'] = [nota['numero'] for nota in notas_sped_que_nao_estao_no_sefaz]
    
    if len(notas_sped_que_nao_estao_no_sefaz) == 0:
        df_notas_sped_que_nao_estao_no_sefaz = pd.DataFrame({'Chave da nota': ['Nenhuma nota encontrada']})
    
    
    return df_notas_sped_que_nao_estao_no_sefaz

def getTableNotasSefazQueNaoEstaoNoSped(notas_sefaz_que_nao_estao_no_sped) -> pd.DataFrame:
    # Notas SEFAZ que não estão no SPED
    
    df_notas_sefaz_que_nao_estao_no_sped = pd.DataFrame(
        {
            'Chave da nota': [nota['Chave_NF-e'] for nota in notas_sefaz_que_nao_estao_no_sped],
            'Número da nota': [nota['Numero'] for nota in notas_sefaz_que_nao_estao_no_sped],
            'Data': [nota['dt_Emit'] for nota in notas_sefaz_que_nao_estao_no_sped],
            'Valor': [nota['Total_NF-e'] for nota in notas_sefaz_que_nao_estao_no_sped],
            'CNPJ do emitente': [nota['CNPJ_Emit'] for nota in notas_sefaz_que_nao_estao_no_sped]
        }
    )
    
    if len(notas_sefaz_que_nao_estao_no_sped) == 0:
        df_notas_sefaz_que_nao_estao_no_sped = pd.DataFrame(
            {
                'Chave da nota': ['Nenhuma nota encontrada'],
                'Número da nota': [''],
                'Data': [''],
                'Valor': [''],
                'CNPJ do emitente': ['']
            }
        )
        
    return df_notas_sefaz_que_nao_estao_no_sped

def getTableNotasSefazESpedDivergenciaTotal(notas_sefaz_e_sped) -> pd.DataFrame:
    # Notas SEFAZ e SPED com divergência no total
    
    df_notas_sefaz_e_sped = pd.DataFrame(
        {
            'Chave da nota': [nota['sefaz']['Chave_NF-e'] for nota in notas_sefaz_e_sped],
            'Número da nota': [nota['sefaz']['Numero'] for nota in notas_sefaz_e_sped],
            'Data': [nota['sefaz']['dt_Emit'] for nota in notas_sefaz_e_sped],
            'Valor SEFAZ': [nota['total_sefaz'] for nota in notas_sefaz_e_sped],
            'Valor SPED': [nota['total_sped'] for nota in notas_sefaz_e_sped],
            'Diferença': [nota['diferenca_total'] for nota in notas_sefaz_e_sped]
        }
    )

    # Remove notas que não possuem divergência
    df_notas_sefaz_e_sped = df_notas_sefaz_e_sped[df_notas_sefaz_e_sped['Diferença'] != 0]
    
    if df_notas_sefaz_e_sped.empty:
        df_notas_sefaz_e_sped = pd.DataFrame(
            {
                'Chave da nota': ['Nenhuma nota que está no SEFAZ e no SPED e possui divergência no total'],
                'Número da nota': [''],
                'Data': [''],
                'Valor SEFAZ': [''],
                'Valor SPED': [''],
                'Diferença': ['']
            }
        )
        
    return df_notas_sefaz_e_sped

def getTableNotasSefazESpedDivergenciaIcms(notas_sefaz_e_sped):
    # Notas SEFAZ e SPED com divergência no ICMS
    
    df_notas_sefaz_e_sped = pd.DataFrame(
        {
            'Chave da nota': [nota['sefaz']['Chave_NF-e'] for nota in notas_sefaz_e_sped],
            'Número da nota': [nota['sefaz']['Numero'] for nota in notas_sefaz_e_sped],
            'CFOPs': [nota['sped']['cfops'].strip().replace(' ', ', ') for nota in notas_sefaz_e_sped],
            'Data': [nota['sefaz']['dt_Emit'] for nota in notas_sefaz_e_sped],
            'Icms SEFAZ': [nota['icms_sefaz'] for nota in notas_sefaz_e_sped],
            'Icms SPED': [nota['sped']['total_icms_produtos'] for nota in notas_sefaz_e_sped],
            'Diferença': [nota['diferenca_icms'] for nota in notas_sefaz_e_sped]
        }
    )
    
    # Remove notas que não possuem divergência
    df_notas_sefaz_e_sped = df_notas_sefaz_e_sped[df_notas_sefaz_e_sped['Diferença'] != 0]
    
    if df_notas_sefaz_e_sped.empty:
        df_notas_sefaz_e_sped = pd.DataFrame(
            {
                'Chave da nota': ['Nenhuma nota que está no SEFAZ e no SPED e possui divergência no ICMS'],
                'Número da nota': [''],
                'CFOPs': [''],
                'Data': [''],
                'Icms SEFAZ': [''],
                'Icms SPED': [''],
                'Diferença': ['']
            }
        )
        
    return df_notas_sefaz_e_sped

def auto_adjust_column_width(writer, sheet_name, dataframe):
    worksheet = writer.sheets[sheet_name]
    for col in dataframe.columns:
        max_length = max(dataframe[col].astype(str).map(len).max(), len(col))
        col_idx = dataframe.columns.get_loc(col) + 1
        worksheet.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = max_length + 2

def createRelatorio(comparacao, cnpjs_de_entrada):
    notas_sped_que_nao_estao_no_sefaz = comparacao['notas_sped_que_nao_estao_no_sefaz']
    notas_sefaz_que_nao_estao_no_sped = comparacao['notas_sefaz_que_nao_estao_no_sped']
    notas_sefaz_e_sped = comparacao['notas_sefaz_e_sped']
    
    df_notas_sped_que_nao_estao_no_sefaz = getTableNotasSpedQueNaoEstaoNoSefaz(notas_sped_que_nao_estao_no_sefaz)
    df_notas_sefaz_que_nao_estao_no_sped = getTableNotasSefazQueNaoEstaoNoSped(notas_sefaz_que_nao_estao_no_sped)
    df_divergencia_total = getTableNotasSefazESpedDivergenciaTotal(notas_sefaz_e_sped)
    df_divergencia_icms = getTableNotasSefazESpedDivergenciaIcms(notas_sefaz_e_sped)

    user_folder = os.path.expanduser('~')
    desktop_path = os.path.join(user_folder, 'Desktop')

    desktop_onedrive_path = os.path.join(user_folder, 'OneDrive', 'Ambiente de Trabalho')
    documentos_path = os.path.join(user_folder, 'Documents')
    windows_temp_path = os.path.join('C:', os.sep, 'Windows', 'Temp')

    if not os.path.exists(desktop_path) and os.path.exists(desktop_onedrive_path):
        desktop_path = desktop_onedrive_path
        
    if not os.path.exists(desktop_path) and os.path.exists(documentos_path):
        desktop_path = documentos_path
        
    if not os.path.exists(desktop_path) and os.path.exists(windows_temp_path):
        desktop_path = windows_temp_path
        
    if not os.path.exists(desktop_path):
        msgbox('Não foi possível encontrar a sua área de trabalho. Por favor certifique-se de que a pasta "Desktop" existe na sua pasta de usuário e tente novamente.')
        return
    
    relatorio_path = os.path.join(desktop_path, 'relatorio_comparativo_sefaz_sped.xlsx')
    
    try:
        if os.path.exists(relatorio_path):
            os.remove(relatorio_path)
    except: # noqa
        msgbox('Não foi possível criar o relatório na sua área de trabalho. Verifique se o arquivo não está aberto e tente novamente.')
        return
    
    with pd.ExcelWriter(relatorio_path) as writer:
        df_notas_sped_que_nao_estao_no_sefaz.to_excel(writer, sheet_name='NF SPED fora do SEFAZ', index=False)
        df_notas_sefaz_que_nao_estao_no_sped.to_excel(writer, sheet_name='NF SEFAZ fora do SPED', index=False)
        df_divergencia_total.to_excel(writer, sheet_name='Divergência total', index=False)
        df_divergencia_icms.to_excel(writer, sheet_name='Divergência ICMS', index=False)
        
        auto_adjust_column_width(writer, 'NF SPED fora do SEFAZ', df_notas_sped_que_nao_estao_no_sefaz)
        auto_adjust_column_width(writer, 'NF SEFAZ fora do SPED', df_notas_sefaz_que_nao_estao_no_sped)
        auto_adjust_column_width(writer, 'Divergência total', df_divergencia_total)
        auto_adjust_column_width(writer, 'Divergência ICMS', df_divergencia_icms)
        

    #open file
    os.startfile(relatorio_path)
    
    msgbox('Relatório criado com sucesso e já abri ele para você. Ele está localizado na pasta: \n\n' + relatorio_path)


if __name__ == '__main__':
    arquivo_teste_sefaz = './downloads/sefaz.3.txt'
    arquivo_teste_sped = './downloads/sped_teste.txt'

    notas_sefaz = getNotasFromSefaz(arquivo_teste_sefaz)
    notas_sped, cnpjs_de_entrada = getNotasFromSped(arquivo_teste_sped)

    comparacao = getComparacaoSefazSped(notas_sefaz, notas_sped)

    createRelatorio(comparacao, None)
    


