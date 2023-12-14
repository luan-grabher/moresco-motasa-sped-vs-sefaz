from easygui import fileopenbox, msgbox
import chardet
import codecs
import tqdm

def getArquivoSpedFromUser():
    msgbox('Selecione o arquivo txt do relatório do SPED com as notas')

    return fileopenbox(msg='Selecione o arquivo txt do relatório do SPED com as notas',
                       title='Relatório txt do SPED',
                       default='*.txt',
                       filetypes='*.txt',
                       multiple=False)


def get_encoding_type(xml_path):
    rawdata = open(xml_path, 'rb').read()
    result = chardet.detect(rawdata)
    return result['encoding']
        
def getNotasFromSped(arquivo_sped):
    separador = '|'
    codigo_nota = 'C100'
    codigo_produto = 'C190'

    coluna_codigo_linha = 1
    coluna_tipo_nota = 2
    coluna_numero_nota = 9
    coluna_cfop = 3
    coluna_valor_total = 5
    coluna_icms = 7

    notas = []
    nota_atual = None

    cnpjs_de_entrada = []
    
    encoding_type = get_encoding_type(arquivo_sped)    
    with codecs.open(arquivo_sped, 'r', encoding=encoding_type, errors='ignore') as sped:
        for linha in tqdm.tqdm(sped.readlines(), desc='Lendo arquivo SPED'):
            colunas = linha.split(separador)
            codigo_linha = colunas[coluna_codigo_linha] if len(colunas) > coluna_codigo_linha else None

            if codigo_linha == codigo_nota:
                numero_nota = colunas[coluna_numero_nota] if len(colunas) > coluna_numero_nota else None

                tipo_nota = colunas[coluna_tipo_nota] if len(colunas) > coluna_tipo_nota else None
                is_nota_entrada = tipo_nota == '0'
                cnpj_from_numero_nota = numero_nota[6:20]

                if is_nota_entrada and cnpj_from_numero_nota not in cnpjs_de_entrada:
                    is_cnpj_in_cnpjs_de_entrada = list(filter(lambda cnpj: cnpj == cnpj_from_numero_nota, cnpjs_de_entrada))
                    if len(is_cnpj_in_cnpjs_de_entrada) == 0:
                        cnpjs_de_entrada.append({
                            'cnpj': cnpj_from_numero_nota,
                            'notas': [ numero_nota ]
                        })
                    else:
                        cnpj_de_entrada = is_cnpj_in_cnpjs_de_entrada[0]
                        cnpj_de_entrada['notas'].append(numero_nota)       
                

                nota_atual = {
                    'numero': numero_nota,
                    'produtos': [],
                    'total_icms_produtos': 0
                }

                is_nota_in_notas = list(filter(lambda nota: nota['numero'] == numero_nota, notas))
                if len(is_nota_in_notas) == 0:
                    notas.append(nota_atual)
            
            elif codigo_linha == codigo_produto:
                cfop = colunas[coluna_cfop] if len(colunas) > coluna_cfop else None
                valor_total = colunas[coluna_valor_total] if len(colunas) > coluna_valor_total else None
                icms = colunas[coluna_icms] if len(colunas) > coluna_icms else None

                if nota_atual:
                    nota_atual['produtos'].append({
                        'cfop': cfop,
                        'valor_total': valor_total,
                        'icms': icms
                    })
                    nota_atual['total_icms_produtos'] += round(float(icms.replace(',', '.')), 2)

    return notas, cnpjs_de_entrada

def getNotaSped(notas_sped, numero_nota):
    notas_sped = list(filter(lambda nota: nota['numero'] == numero_nota, notas_sped))
    return notas_sped[0] if len(notas_sped) > 0 else None

if __name__ == '__main__':
    arquivo_sped = './downloads/sped_teste.txt'
    notas, cnpjs_de_entrada = getNotasFromSped(arquivo_sped)
    
    print(len(cnpjs_de_entrada))