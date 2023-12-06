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
    coluna_numero_nota = 9
    coluna_cfop = 3
    coluna_valor_total = 5
    coluna_icms = 7

    notas = []
    nota_atual = None
    
    encoding_type = get_encoding_type(arquivo_sped)
    
    with codecs.open(arquivo_sped, 'r', encoding=encoding_type, errors='ignore') as sped:
        for linha in tqdm.tqdm(sped.readlines(), desc='Lendo arquivo SPED'):
            colunas = linha.split(separador)
            codigo_linha = colunas[coluna_codigo_linha] if len(colunas) > coluna_codigo_linha else None

            if codigo_linha == codigo_nota:
                numero_nota = colunas[coluna_numero_nota] if len(colunas) > coluna_numero_nota else None
                nota_atual = {
                    'numero': numero_nota,
                    'produtos': []
                }

                if nota_atual not in notas and nota_atual:
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

    return notas

def getNotaSped(notas_sped, numero_nota):
    return list(filter(lambda nota: nota['numero'] == numero_nota, notas_sped))[0]

if __name__ == '__main__':
    arquivo_sped = './downloads/sped_teste.txt'
    notas = getNotasFromSped(arquivo_sped)

    nota_validadora = '43231097834188000105550030004688701004980591'
    nota = getNotaSped(notas, nota_validadora)
    
    print(nota)