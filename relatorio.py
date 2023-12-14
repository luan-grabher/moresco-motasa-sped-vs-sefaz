import os
from comparativo import getComparacaoSefazSped

from sefaz import getNotasFromSefaz
from sped import getNotasFromSped


'''
    1. Analise das notas fiscais constantes no arquivo SPED que não constam no sefaz – relação de notas com o número da nota.
    2. Analise das notas fiscais constantes no sefaz que não constam no arquivo SPED – relação de notas trazendo o número da nota, data, valor e CNPJ do emitente.
    3. Analise do total da NFE Sped + campo ICMS x Total da NFE sefaz + campo ICMS – relação de notas divergentes pelo número da nota
    4. Com base no resultado do item 3, fazer a análise individual por nota do arquivo SPED buscando a nota com o CFOP/valor/ ICMS x Sefaz nota e valor ICMS – relação de notas
'''

def getTableNotasSpedQueNaoEstaoNoSefaz(notas_sped_que_nao_estao_no_sefaz):
    html = '<h1>Notas SPED que não estão no SEFAZ</h1>'
    html += '<table style="width:100%">'
    html += '<tr>'
    html += '<th>Número da nota</th>'
    html += '</tr>'
    for nota in notas_sped_que_nao_estao_no_sefaz:
        html += '<tr>'
        html += '<td>{}</td>'.format(nota['numero'])
        html += '</tr>'

    if len(notas_sped_que_nao_estao_no_sefaz) == 0:
        html += '<tr>'
        html += '<td>Nenhuma nota encontrada</td>'
        html += '</tr>'

    html += '</table>'

    return html

def getTableNotasSefazQueNaoEstaoNoSped(notas_sefaz_que_nao_estao_no_sped):
    html = '<h1>Notas SEFAZ que não estão no SPED</h1>'
    html += '<table style="width:100%">'
    html += '<tr>'
    html += '<th>Número da nota</th>'
    html += '<th>Data</th>'
    html += '<th>Valor</th>'
    html += '<th>CNPJ do emitente</th>'
    html += '</tr>'
    for nota in notas_sefaz_que_nao_estao_no_sped:
        html += '<tr>'
        html += '<td>{}</td>'.format(nota['Chave_NF-e'])
        html += '<td>{}</td>'.format(nota['dt_Emit'])
        html += '<td>{}</td>'.format(nota['Total_NF-e'])
        html += '<td>{}</td>'.format(nota['CNPJ_Emit'])
        html += '</tr>'
    
    if len(notas_sefaz_que_nao_estao_no_sped) == 0:
        html += '<tr>'
        html += '<td>Nenhuma nota encontrada</td>'
        html += '</tr>'
    
    html += '</table>'

    return html

def getTableNotasSefazESpedDivergenciaTotal(notas_sefaz_e_sped):
    html = '<h1>Notas SEFAZ e SPED com divergência no total</h1>'
    html += '<table style="width:100%">'
    html += '<tr>'
    html += '<th>Número da nota</th>'
    html += '<th>Data</th>'
    html += '<th>Valor SEFAZ</th>'
    html += '<th>Valor SPED</th>'
    html += '<th>Diferença</th>'
    html += '</tr>'
    for nota in notas_sefaz_e_sped:
        if nota['diferenca_total'] == 0:
            continue

        html += '<tr>'
        html += '<td>{}</td>'.format(nota['sefaz']['Chave_NF-e'])
        html += '<td>{}</td>'.format(nota['sefaz']['dt_Emit'])
        html += '<td>{}</td>'.format(nota['total_sefaz'])
        html += '<td>{}</td>'.format(nota['total_sped'])
        html += '<td>{}</td>'.format(nota['diferenca_total'])
        html += '</tr>'
    
    if len(notas_sefaz_e_sped) == 0:
        html += '<tr>'
        html += '<td>Nenhuma nota encontrada</td>'
        html += '</tr>'
    
    html += '</table>'

    return html

def getTableNotasSefazESpedDivergenciaIcms(notas_sefaz_e_sped):
    html = '<h1>Notas SEFAZ e SPED com divergência no ICMS</h1>'
    html += '<table style="width:100%">'
    html += '<tr>'
    html += '<th>Número da nota</th>'
    html += '<th>Data</th>'
    html += '<th>Icms SEFAZ</th>'
    html += '<th>Icms SPED</th>'
    html += '<th>Diferença</th>'
    html += '</tr>'
    for nota in notas_sefaz_e_sped:
        if nota['diferenca_icms'] == 0:
            continue

        html += '<tr>'
        html += '<td>{}</td>'.format(nota['sefaz']['Chave_NF-e'])
        html += '<td>{}</td>'.format(nota['sefaz']['dt_Emit'])
        html += '<td>{}</td>'.format(nota['icms_sefaz'])
        html += '<td>{}</td>'.format(nota['sped']['total_icms_produtos'])
        html += '<td>{}</td>'.format(nota['diferenca_icms'])
        html += '</tr>'
    
    if len(notas_sefaz_e_sped) == 0:
        html += '<tr>'
        html += '<td>Nenhuma nota encontrada</td>'
        html += '</tr>'
    
    html += '</table>'

    return html

def createRelatorio(comparacao):
    notas_sped_que_nao_estao_no_sefaz = comparacao['notas_sped_que_nao_estao_no_sefaz']
    notas_sefaz_que_nao_estao_no_sped = comparacao['notas_sefaz_que_nao_estao_no_sped']
    notas_sefaz_e_sped = comparacao['notas_sefaz_e_sped']

    html = '<html>'
    html += '<head>'
    html += '<style>'
    html += 'table, th, td {'
    html += 'border: 1px solid black;'
    html += 'border-collapse: collapse;'
    html += '}'
    html += 'th, td {'
    html += 'padding: 5px;'
    html += '}'
    html += '</style>'
    html += '</head>'
    html += '<body>'

    html += getTableNotasSpedQueNaoEstaoNoSefaz(notas_sped_que_nao_estao_no_sefaz)
    html += getTableNotasSefazQueNaoEstaoNoSped(notas_sefaz_que_nao_estao_no_sped)
    html += getTableNotasSefazESpedDivergenciaTotal(notas_sefaz_e_sped)
    html += getTableNotasSefazESpedDivergenciaIcms(notas_sefaz_e_sped)

    html += '</body>'
    html += '</html>'
    
    nome_relatorio = 'relatorio_comparativo_sefaz_sped.html'
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    arquivo_relatorio = os.path.join(desktop, nome_relatorio)
    with open(arquivo_relatorio, 'w') as arquivo:
        arquivo.write(html)

    #open file
    os.startfile(arquivo_relatorio)    


if __name__ == '__main__':
    arquivo_teste_sefaz = './downloads/sefaz.txt'
    arquivo_teste_sped = './downloads/sped_teste.txt'

    notas_sefaz = getNotasFromSefaz(arquivo_teste_sefaz)
    notas_sped, cnpjs_de_entrada = getNotasFromSped(arquivo_teste_sped)

    comparacao = getComparacaoSefazSped(notas_sefaz, notas_sped)

    createRelatorio(comparacao)
    


