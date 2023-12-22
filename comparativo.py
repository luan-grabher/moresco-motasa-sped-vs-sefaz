import tqdm
from sefaz import getNotaSefaz, getNotasFromSefaz

from sped import getNotaSped, getNotasFromSped


def getComparacaoSefazSped(notas_sefaz, notas_sped):
    notas_sped_que_nao_estao_no_sefaz = []
    notas_sefaz_que_nao_estao_no_sped = []
    notas_sefaz_e_sped = []

    for index, nota_sefaz in tqdm.tqdm(notas_sefaz.iterrows(), desc='Comparando notas SEFAZ e SPED'):
        chave_nfe = nota_sefaz['Chave_NF-e']
        if not chave_nfe or chave_nfe == '':
            continue

        nota_sped = getNotaSped(notas_sped, chave_nfe)

        if not nota_sped:
            notas_sefaz_que_nao_estao_no_sped.append(nota_sefaz)
        else:
            icms_sefaz = round(float(nota_sefaz['Total_ICMS'].replace(',', '.')), 2)
            diferenca_icms = round(icms_sefaz - nota_sped['total_icms_produtos'], 2)
            
            total_sefaz = float(nota_sefaz['Total_NF-e'].replace(',', '.'))

            total_sped = sum([float(produto['valor_total'].replace(',', '.')) for produto in nota_sped['produtos']])
            total_sped = round(total_sped, 2)

            diferenca_total = round(total_sefaz - total_sped, 2)

            notas_sefaz_e_sped.append({
                'sefaz': nota_sefaz.to_dict(),
                'sped': nota_sped,
                'diferenca_icms': diferenca_icms,
                'diferenca_total': diferenca_total,
                'total_sefaz': total_sefaz,
                'total_sped': total_sped,
                'icms_sefaz': icms_sefaz,
            })


    for nota_sped in tqdm.tqdm(notas_sped, desc='Comparando notas SPED e SEFAZ'):
        chave_nfe = nota_sped['numero']
        if not chave_nfe or chave_nfe == '':
            continue

        nota_sefaz = getNotaSefaz(notas_sefaz, chave_nfe)

        if nota_sefaz.empty:
            notas_sped_que_nao_estao_no_sefaz.append(nota_sped)

    return {
        'notas_sped_que_nao_estao_no_sefaz': notas_sped_que_nao_estao_no_sefaz,
        'notas_sefaz_que_nao_estao_no_sped': notas_sefaz_que_nao_estao_no_sped,
        'notas_sefaz_e_sped': notas_sefaz_e_sped
    }


if __name__ == '__main__':
    arquivo_teste_sefaz = './downloads/sefaz.txt'
    arquivo_teste_sped = './downloads/sped_teste.txt'

    notas_sefaz = getNotasFromSefaz(arquivo_teste_sefaz)
    notas_sped, cnpjs_de_entrada = getNotasFromSped(arquivo_teste_sped)

    comparacao = getComparacaoSefazSped(notas_sefaz, notas_sped)

    print(comparacao['notas_com_diferenca_icms'])