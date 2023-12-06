import tqdm
from sefaz import getNotasFromSefaz

from sped import getNotaSped, getNotasFromSped


def getComparacaoSefazSped(notas_sefaz, notas_sped):
    notas_sped_que_nao_estao_no_sefaz = []
    notas_sefaz_que_nao_estao_no_sped = []
    notas_sefaz_e_sped = []

    for index, nota_sefaz in tqdm.tqdm(notas_sefaz.iterrows(), desc='Comparando notas SEFAZ e SPED'):
        chave_nfe = nota_sefaz['Chave_NF-e']
        nota_sped = getNotaSped(notas_sped, chave_nfe)

        if not nota_sped:
            notas_sefaz_que_nao_estao_no_sped.append(nota_sefaz)
        else:
            notas_sefaz_e_sped.append({
                'sefaz': nota_sefaz.to_dict(),
                'sped': nota_sped
            })

    return {
        'notas_sped_que_nao_estao_no_sefaz': notas_sped_que_nao_estao_no_sefaz,
        'notas_sefaz_que_nao_estao_no_sped': notas_sefaz_que_nao_estao_no_sped,
        'notas_sefaz_e_sped': notas_sefaz_e_sped
    }


if __name__ == '__main__':
    arquivo_teste_sefaz = './downloads/sefaz.txt'
    arquivo_teste_sped = './downloads/sped_teste.txt'

    notas_sefaz = getNotasFromSefaz(arquivo_teste_sefaz)
    notas_sped = getNotasFromSped(arquivo_teste_sped)

    comparacao = getComparacaoSefazSped(notas_sefaz, notas_sped)

    print(comparacao['notas_sefaz_e_sped'])