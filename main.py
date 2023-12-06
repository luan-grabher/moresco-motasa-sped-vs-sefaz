#[X]:Usuario escolhe arquivo sped
#[X]: Usuario escolhe arquivo sefaz
#[ ]:  (Opcional) Usuario pode escolher mais de uma pasta e o robo seelciona [ ]s arquivos .txt que tenham as colunas do sefaz separadas por ; e junta [ ]s em um array só. (Caso fizer deixa em stand by comentado e pergunta para elas se é assim ou não)
#[ ]: Extrai dados do sped → notas + produtos da nota
#[x]: Extrai dados do sefaz
#[ ]: Lista de notas do sped que não existem no sefaz
#[ ]: Lista de notas no sefaz que nao existem no sped
#[ ]: Lista de notas no sefaz e no sped
#[ ]: Comparar valores totais das notas sefaz com soma do icms dos produtos do sped conforme lista de notas que estao nos dois arquivos
#[ ]: Relatório em HTML com os comparativos
#[ ]: Salvar relatório HTML no desktop e abrir o arquivo após a conclusão do programa
#[ ]: Testes
#[ ]: Criação de instalador

import os

os.system('python -m pip install --upgrade pip')
os.system('pip install -r requirements.txt')
os.system('cls')

from sped_vs_sefaz import sped_vs_sefaz

sped_vs_sefaz()